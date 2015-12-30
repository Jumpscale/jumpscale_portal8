import urllib.request, urllib.parse, urllib.error
import requests

from JumpScale import j
try:
    import ujson as json
except:
    import json

class system_oauth(j.tools.code.classGetBase()):
    """
    Oauth System actors
    """
    def authenticate(self, type='', **kwargs):
        cache = j.clients.redis.getByInstance('system')

        if j.core.portal.active.force_oauth_instance:
            type = j.core.portal.active.force_oauth_instance

        if not type:
            type = 'github'
        
        ctx = kwargs['ctx']
        redirect = kwargs.get('redirect', '/')
        client = j.clients.oauth.get(instance=type)
        cache_data = json.dumps({'type' : type, 'redirect' : redirect})
        cache.set(client.state,cache_data , ex=180)
        ctx.start_response('302 Found', [('Location', client.url)])
        return 'OK'
    
    def getOauthLogoutURl(self, **kwargs):
        ctx = kwargs['ctx']
        redirecturi = ctx.env.get('HTTP_REFERER')
        if not redirecturi:
            redirecturi = 'http://%s'% ctx.env['HTTP_HOST']
        session = ctx.env['beaker.session']
        if session:
            oauth = session.get('oauth')
            session.delete()
            session.save()
            if oauth:
                back_uri = urllib.parse.urlencode({'redirect_uri': redirecturi})
                location = str('%s?%s'% (oauth.get('logout_url'), back_uri))
                ctx.start_response('302 Found', [('Location', location)])
            else:
                ctx.start_response('302 Found', [('Location', redirecturi)])
        else:
            ctx.start_response('302 Found', [('Location', redirecturi)])
        return ''

    def authorize(self, **kwargs):
        ctx = kwargs['ctx']
        code = kwargs.get('code')
        if not code:
            ctx.start_response('403 Not Authorized', [])
            return 'Not Authorized -- Code is missing'
        
        state = kwargs.get('state')
        if not state:
            ctx.start_response('403 Not Authorized', [])
            return 'Not Authorized -- State is missing'
        
        cache = j.clients.redis.getByInstance('system')
        cache_result = cache.get(state)
        
        if not cache_result:
            unauthorized_redirect_url = '%s?%s' % ('/restmachine/system/oauth/authenticate', urllib.parse.urlencode({'type': j.core.portal.active.force_oauth_instance or 'github'}))
            msg = 'Not Authorized -- Invalid or expired state'
            j.logger.log(msg)
            ctx.start_response('302 Found', [('Location', unauthorized_redirect_url)])
            return msg
        
        cache_result = json.loads(cache_result)
        client = j.clients.oauth.get(instance=cache_result['type'])
        payload = {'code': code, 'client_id': client.id, 'client_secret': client.secret, 'redirect_uri': client.redirect_url, 'grant_type':'authorization_code'}
        result = requests.post(client.accesstokenaddress, data=payload, headers={'Accept': 'application/json'})
        
        if not result.ok or 'error' in result.json():
            msg = 'Not Authorized -- %s' % result.json()['error']
            j.logger.log(msg)
            ctx.start_response('403 Not Authorized', [])
            return msg
        
        result = result.json()
        access_token = result['access_token']
        params = {'access_token' : access_token}
        userinfo = requests.get('%s?%s' % (client.user_info_url, urllib.parse.urlencode(params))).json()
        username = userinfo['login']
        email = userinfo['email']

        user_model = j.data.models.User
        user_obj = j.data.models.User.find({'name':username})

        if not user_obj:
            # register user
            u = user_model()
            u.name = username
            u.emails = [email]
            u.save()
        else:
            u = user_obj[0]
            if email not in u['emails']:
              ctx.start_response('400 Bad Request', [])
              return 'User witht the same name already exists'         

        session = ctx.env['beaker.session']
        session['user'] = username
        session['email'] = email
        session['oauth'] = {'authorized':True, 'type':str(cache_result['type']), 'logout_url':client.logout_url}
        session._redis = True
        session.save()
        
        ctx.start_response('302 Found', [('Location', str(cache_result['redirect']))])
