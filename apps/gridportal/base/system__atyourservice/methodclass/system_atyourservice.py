from JumpScale import j


class system_atyourservice(j.tools.code.classGetBase()):

    """
    gateway to atyourservice
    """

    def __init__(self):
        pass

        self._te = {}
        self.actorname = "atyourservice"
        self.appname = "system"
        # system_atyourservice_osis.__init__(self)
        self._rest_client = None

    def get_client(self, **kwargs):
        if self._rest_client is None:
            ctx = kwargs['ctx']
            username = ctx.env['beaker.session']['user']
            qs = j.data.models.oauth.JWTToken.find({'username': username, 'expire': {'$gt': j.data.time.epoch}})
            if qs.count() <= 0:
                # no JWT token valid in DB, generate a new one.
                token = j.apps.system.oauthtoken.generateJwtToken(scope='', audience='', **kwargs)
            else:
                # JWT available, use this one
                token = qs.first()

            cockpit_cfg = j.portal.server.active.cfg['cockpit']
            base_url = "http://{host}:{port}".format(**cockpit_cfg)
            self._rest_client = j.clients.cockpit.getClient(base_url, token['jwt_token'])
        return self._rest_client

    def listRepos(self):
        return j.atyourservice.repos.keys()

    def listServices(self, repo_path=None, role=None, templatename=None, **kwargs):
        """
        list all services
        param:name services in that base name will only be returned otherwise all names
        result json of {aysname:services}
        """
        services = dict()
        repos = [repo_path] if repo_path else self.listRepos()

        for aysrepo in repos:
            repo = j.atyourservice.repos[aysrepo]
            if role:
                services.update({aysrepo: {shortkey: service for shortkey, service in repo.services.items() if service.role == role}})
            elif templatename:
                services.update({aysrepo: {shortkey: service for shortkey, service in repo.services.items() if service.templatename == templatename}})
            else:
                services.update({aysrepo: repo.services})
        return services

    def listBlueprints(self, repo_path=None, **kwargs):
        """
        list all blueprints
        param:name blueprints in that base name will only be returned otherwise all names
        result json
        """
        blueprints = dict()
        repos = [repo_path] if repo_path else self.listRepos()

        for aysrepo in repos:
            repo = j.atyourservice.repos[aysrepo]
            blueprints.update({aysrepo: repo.blueprints})

        return blueprints

    def listTemplates(self, repo_path=None, **kwargs):
        """
        list all templates of a certain type
        param:role template role
        param:name templates in that base name will only be returned otherwise all names
        result json
        """
        templates = dict()
        repos = [repo_path] if repo_path else self.listRepos()

        for aysrepo in repos:
            repo = j.atyourservice.repos[aysrepo]
            templates.update({aysrepo: repo.templates})
        return templates

    def findServices(self, repo_name, role='', templatename='', instance='', **kwargs):
        repo = j.atyourservice.repos[repo_name]
        return repo.findServices(role=role, instance=instance, templatename=templatename)

    def reload(self, **kwargs):
        cl = self.get_client(**kwargs)
        cl.reloadAll()
        return {'msg': 'service reloaded'}
