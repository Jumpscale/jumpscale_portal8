import urllib.request
import urllib.parse
import urllib.error
import requests
import json
from JumpScale import j
from JumpScale.portal.portal import exceptions


class system_oauth(j.tools.code.classGetBase()):
    """
    Oauth System actors
    """

    def __init__(self):
        self.logger = j.logger.get("j.portal.oauth")
        self.cfg = j.portal.server.active.cfg
        self._client = None

    @property
    def client(self):
        if not self._client:
            self._client = j.clients.oauth.get(addr=self.cfg.get('client_url'), accesstokenaddr=self.cfg.get('token_url'), id=self.cfg.get('client_id'),
                                     secret=self.cfg.get('client_secret'), scope=self.cfg.get('client_scope'), redirect_url=self.cfg.get('redirect_url'),
                                     user_info_url=self.cfg.get('client_user_info_url'), logout_url='')
        return self._client

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
        session = ctx.env['beaker.session']
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

        def authfailure(msg):
            session['autherror'] = msg
            session._redis = True
            session.save()
            self.logger.warn(msg)
            raise exceptions.Redirect(str(cache_result['redirect']))

        if not cache_result:
            msg = 'Failed to authenticate. Invalid or expired state'
            return authfailure(msg)

        cache_result = j.data.serializer.json.loads(cache_result)

        # generate access_token
        payload = {'client_id': self.client.id, 'client_secret': self.client.secret, 'code': code, 'state': state, 'redirect_uri': self.client.redirect_url}
        access_token_resp = requests.post(self.client.accesstokenaddress, data=payload, headers={'Accept': 'application/json'})

        if not access_token_resp.ok or 'error' in access_token_resp.text:
            msg = 'Not Authorized -- %s' % access_token_resp.text
            self.logger.warn(msg)
            autherror = "Error happened during authentication please try again or contact your administrator."
            return authfailure(autherror)

        access_token_data = access_token_resp.json()
        if access_token_data['scope'] != self.cfg['client_scope']:
            msg = 'Failed to get the requested scope for %s' % self.client.id
            return authfailure(msg)

        access_token = access_token_data['access_token']
        if cache_result.get('type', 'github') == 'itsyou.online':
            username = access_token_data['info'].get('username', 'admin')
            url = self.client.user_info_url + "/%s/info" % username
        else:
            url = self.client.user_info_url

        user_info_resp = requests.get(url, headers={'Authorization': 'token %s' % access_token})
        if not user_info_resp.ok:
            msg = "Can't retreive info for user -- %s" % user_info_resp.text
            return authfailure(msg)

        userinfo = user_info_resp.json()
        username = userinfo.get(
            'username',
            userinfo.get('login')
        )
        email = None
        if 'email' in userinfo:
            if j.data.types.string.check(userinfo['email']):
                email = userinfo['email']
            elif j.data.types.dict.check(userinfo['email']):
                d = userinfo['email'].values()
                email = list(d)[0]
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
                return authfailure('User with the same name already exists')

        session = ctx.env['beaker.session']
        session['user'] = username
        if email:
            session['email'] = email
        session['oauth'] = {
            'authorized': True,
            'type': str(cache_result['type']),
            'logout_url': self.client.logout_url,
            'access_token': access_token
        }
        session.pop('autherror', None)
        session['_expire_at'] = j.data.time.epoch + access_token_data['expires_in']
        session.save()

        raise exceptions.Redirect(str(cache_result['redirect']))
