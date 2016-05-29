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

    def listRepos(self):
        return j.atyourservice.repos.keys()

    def listServices(self, name=None, **kwargs):
        """
        list all services
        param:name services in that base name will only be returned otherwise all names
        result json of {aysname:services}
        """
        services = dict()
        names = [name] if name else self.listRepos()

        for aysname in names:
            repo = j.atyourservice.repos[aysname]
            services.update({aysname: repo.services})

        return services

    def listBlueprints(self, name=None, **kwargs):
        """
        list all blueprints
        param:name blueprints in that base name will only be returned otherwise all names
        result json
        """
        services = dict()
        names = [name] if name else self.listRepos()

        for aysname in names:
            repo = j.atyourservice.repos[aysname]
            services.update({aysname: repo.blueprints})

        return services

    def listServicesByRole(self, role, name=None, **kwargs):
        """
        list all services of a certain type
        param:role service role
        param:name services in that base name will only be returned otherwise all names
        result json
        """
        services = dict()
        names = [name] if name else self.listRepos()

        for aysname in names:
            repo = j.atyourservice.repos[aysname]
            services.update({aysname: [service for _, service in repo.services.items() if service.role == role]})
        return services

    def listTemplates(self ,name=None, **kwargs):
        """
        list all templates of a certain type
        param:role template role
        param:name templates in that base name will only be returned otherwise all names
        result json
        """
        templates = dict()
        names = [name] if name else self.listRepos()

        for aysname in names:
            repo = j.atyourservice.repos[aysname]
            templates.update({aysname: repo.templates})
        return templates
