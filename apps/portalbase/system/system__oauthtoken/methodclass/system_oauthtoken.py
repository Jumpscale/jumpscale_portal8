from JumpScale import j
import requests
import urllib


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

        # save JWT
        jwt = j.data.models.oauth.JWTToken()
        jwt.jwt_token = resp.text
        jwt.username = ctx.env['beaker.session']['user']
        jwt.save()

        return jwt.to_dict()

    def getJWTToken(self, token, **kwargs):
        """
        param:key redis key of the token
        result json
        """
        token = j.data.models.oauth.AccessToken.find({'access_token': token}).first()
        if token:
            return token.to_dict()

    def listJWTTokens(self, **kwargs):
        """
        result json
        """
        output = []
        for token in j.data.models.oauth.JWTToken.find({'expire': {'$gt': j.data.time.epoch}}):
            output.append(token.to_dict())
        return output
