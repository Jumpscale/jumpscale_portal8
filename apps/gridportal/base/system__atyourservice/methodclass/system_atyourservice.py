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

    def listServices(self, path=None, **kwargs):
        """
        list all services
        param:path services in that base path will only be returned otherwise all paths
        result json
        """
        services = dict()

        def _getServicesInPath(path):
            j.atyourservice.basepath = ayspath
            services.update({path: j.atyourservice.services})

        if path:
            _getServicesInPath(path)
            return services

        for tree in j.sal.fs.listFilesInDir(j.sal.fs.joinPaths(j.dirs.varDir, 'servicetrees')):
            ayspath = j.sal.fs.getBaseName(tree.rsplit('.json', 1)[0]).replace('__', '/')
            _getServicesInPath(ayspath)
        return services

    def listBlueprints(self, path=None, **kwargs):
        """
        list all blueprints
        param:path blueprints in that base path will only be returned otherwise all paths
        result json
        """
        services = dict()

        def _getBPInPath(path):
            j.atyourservice.basepath = ayspath
            services.update({path: j.atyourservice.blueprints})

        if path:
            _getBPInPath(path)
            return services

        for tree in j.sal.fs.listFilesInDir(j.sal.fs.joinPaths(j.dirs.varDir, 'servicetrees')):
            ayspath = j.sal.fs.getBaseName(tree.rsplit('.json', 1)[0]).replace('__', '/')
            _getBPInPath(ayspath)
        return services

    def listServicesByRole(self, role, path=None, **kwargs):
        """
        list all services of a certain type
        param:role service role
        param:path services in that base path will only be returned otherwise all paths
        result json
        """
        services = dict()

        def _getServicesInPath(path, role):
            j.atyourservice.basepath = ayspath
            services.update({path: [service for _, service in j.atyourservice.services.items() if service.role == role]})
        if path:
            _getServicesInPath(path, role)
            return services

        for tree in j.sal.fs.listFilesInDir(j.sal.fs.joinPaths(j.dirs.varDir, 'servicetrees')):
            ayspath = j.sal.fs.getBaseName(tree.rsplit('.json', 1)[0]).replace('__', '/')
            _getServicesInPath(ayspath, role)
        return services

    def listTemplates(self):
        return j.atyourservice.templates
