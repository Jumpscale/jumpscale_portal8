import urllib.request
import urllib.parse
import urllib.error
import requests
import json
from JumpScale.portal.portal import exceptions
from JumpScale import j


class system_oauth(j.tools.code.classGetBase()):
    """
    Oauth System actors
    """

    def __init__(self):
        self.logger = j.logger.get("j.portal.oauth")
        self.cfg = j.portal.server.active.cfg
        self.client = j.clients.oauth.get(addr=self.cfg.get('client_url'), accesstokenaddr=self.cfg.get('token_url'), id=self.cfg.get('client_id'),
                                     secret=self.cfg.get('client_secret'), scope=self.cfg.get('client_scope'), redirect_url=self.cfg.get('redirect_url'),
                                     user_info_url=self.cfg.get('client_user_info_url'), logout_url='')

    def authenticate(self, type='', **kwargs):
        cache = j.core.db

        if j.portal.server.active.force_oauth_instance:
            type = j.portal.server.active.force_oauth_instance

        if not type:
            type = 'github'

        ctx = kwargs['ctx']

        cache_data = json.dumps({'type': type, 'redirect': ctx.env.get('HTTP_REFERER', '/')})
        cache.set(self.client.state, cache_data, ex=180)
        ctx.start_response('302 Found', [('Location', self.client.url)])
        return 'OK'

    def getOauthLogoutURl(self, **kwargs):
        ctx = kwargs['ctx']
        redirecturi = ctx.env.get('HTTP_REFERER')
        if not redirecturi:
            redirecturi = 'http://%s' % ctx.env['HTTP_HOST']
        session = ctx.env['beaker.session']
        if session:
            oauth = session.get('oauth')
            session.delete()
            session.save()
            if oauth:
                back_uri = urllib.parse.urlencode({'redirect_uri': redirecturi})
                location = str('%s?%s' % (oauth.get('logout_url'), back_uri))
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

        cache = j.core.db
        cache_result = cache.get(state)
        cache.delete(state)

        if not cache_result:
            unauthorized_redirect_url = '%s?%s' % ('/restmachine/system/oauth/authenticate',
                                                   urllib.parse.urlencode({'type': j.portal.server.active.force_oauth_instance or 'github'}))
            msg = 'Not Authorized -- Invalid or expired state'
            self.logger.warn(msg)
            ctx.start_response('302 Found', [('Location', unauthorized_redirect_url)])
            return msg

        cache_result = j.data.serializer.json.loads(cache_result)

        payload = {'client_id': self.client.id, 'client_secret': self.client.secret, 'code': code, 'state': state, 'redirect_uri': self.client.redirect_url}
        result = requests.post(self.client.accesstokenaddress, data=payload, headers={'Accept': 'application/json'})

        if not result.ok or 'error' in result.text:
            msg = 'Not Authorized -- %s' % result.text
            self.logger.warn(msg)
            ctx.start_response('403 Not Authorized', [])
            return msg

        result = result.json()
        if result['scope'] != self.cfg['client_scope']:
            msg = 'Not Authorized -- wrong scope'
            self.logger.warn(msg)
            ctx.start_response('403 Not Authorized', [])
            return msg

        access_token = result['access_token']
        if cache_result.get('type', 'github') == 'itsyou.online':
            username = result['info'].get('username', 'admin')
            url = self.client.user_info_url + "/%s/info" % username
        else:
            url = self.client.user_info_url

        result = requests.get(url, headers={'Authorization': 'token %s' % access_token})
        if not result.ok:
            msg = "Can't retreive info for user -- %s" % result.text
            self.logger.warn(msg)
            ctx.start_response('500 Internal Server Error', [])
            return msg

        userinfo = result.json()
        username = userinfo.get(
            'username',
            userinfo.get('login')
        )
        if 'email' in userinfo:
            if j.data.types.string.check(userinfo['email']):
                email = userinfo['email']
            elif j.data.types.dict.check(userinfo['email']):
                d = userinfo['email'].values()
                email = list(d)[0]
            else:
                email = None
        user_model = j.data.models.system.User
        user_obj = user_model.find({'name': username})

        if not user_obj:
            # register user
            u = user_model()
            u.name = username
            if email:
                u.emails = [email]
            u.groups.extend(self.cfg.get('oauth.default_groups', ['user']))
            u.save()
        else:
            u = user_obj[0]
            if username != u['name']:
                ctx.start_response('400 Bad Request', [])
                return 'User with the same name already exists'

        session = ctx.env['beaker.session']
        session['user'] = username
        if email:
            session['email'] = email
        session['oauth'] = {'authorized': True, 'type': str(cache_result['type']), 'logout_url': self.client.logout_url}
        session._redis = True
        session.save()

        ctx.start_response('302 Found', [('Location', str(cache_result['redirect']))])
