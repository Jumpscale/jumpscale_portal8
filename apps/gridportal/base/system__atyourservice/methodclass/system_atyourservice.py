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
