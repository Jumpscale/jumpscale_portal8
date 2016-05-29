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
        return j.atyourservice.findAYSRepos()

    def listServices(self, path=None, **kwargs):
        """
        list all services
        param:path services in that base path will only be returned otherwise all paths
        result json of {ayspath:services}
        """
        services = dict()
        paths = [path] if path else j.atyourservice.findAYSRepos()

        for ayspath in paths:
            repo = j.atyourservice.get(ayspath)
            services.update({ayspath: repo.services})

        return services

    def listBlueprints(self, path=None, **kwargs):
        """
        list all blueprints
        param:path blueprints in that base path will only be returned otherwise all paths
        result json
        """
        services = dict()
        paths = [path] if path else j.atyourservice.findAYSRepos()

        for ayspath in paths:
            repo = j.atyourservice.get(ayspath)
            services.update({ayspath: repo.blueprints})

        return services

    def listServicesByRole(self, role, path=None, **kwargs):
        """
        list all services of a certain type
        param:role service role
        param:path services in that base path will only be returned otherwise all paths
        result json
        """
        services = dict()
        paths = [path] if path else j.atyourservice.findAYSRepos()

        for ayspath in paths:
            repo = j.atyourservice.get(ayspath)
            services.update({ayspath: [service for _, service in repo.services.items() if service.role == role]})
        return services

    def listTemplates(self ,path=None, **kwargs):
        """
        list all templates of a certain type
        param:role template role
        param:path templates in that base path will only be returned otherwise all paths
        result json
        """
        templates = dict()
        paths = [path] if path else [''] + list(j.atyourservice.findAYSRepos())

        for ayspath in paths:
            repo = j.atyourservice.get(ayspath) if ayspath else j.atyourservice
            templates.update({ayspath: repo.templates})
        return templates
