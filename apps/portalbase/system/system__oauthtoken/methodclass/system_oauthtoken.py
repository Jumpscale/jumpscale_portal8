from JumpScale import j
import requests
import urllib
import jwt as libjwt


class system_oauthtoken(j.tools.code.classGetBase()):

    def __init__(self):
        pass

        self._te = {}
        self.actorname = "oauthtoken"
        self.appname = "system"

    def generateJwtToken(self, scope, audience, **kwargs):
        ctx = kwargs['ctx']

        oauth_ctx = ctx.env['beaker.session'].get('oauth', None)
        if oauth_ctx is None:
            raise j.exceptions.RuntimeError("No oauth information in session")

        access_token = oauth_ctx.get('access_token', None)
        if access_token is None:
            raise j.exceptions.RuntimeError("No access_token in session")

        # make sure we have the required scope and audience in the JWT
        organization = j.portal.server.active.cfg['organization']
        scope = scope.split(',') if scope else []
        memberOf = "user:memberof:%s" % organization
        if memberOf not in scope:
            scope.append(memberOf)

        audience = audience.split(',') if audience else []
        if organization not in audience:
            audience.append(organization)

        # generate JWT
        params = {
            'scope': ','.join(scope),
            'aud': ','.join(audience)
        }
        headers = {'Authorization': 'token ' + access_token}
        url = 'https://itsyou.online/v1/oauth/jwt?%s' % urllib.parse.urlencode(params)
        resp = requests.post(url, headers=headers, verify=False)
        resp.raise_for_status()

        return resp.text
