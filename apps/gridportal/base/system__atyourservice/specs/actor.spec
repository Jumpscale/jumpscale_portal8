[actor] @dbtype:mem,fs
    """
    gateway to atyourservice
    """
    method:listServices
        """
        list all services
        """
        var:repo_path str,,services in that base path will only be returned otherwise all paths @tags: optional
        var:templatename str,, only services with this templatename else all service names @tags: optional
        var:role str,, only services with this role else all service names @tags: optional
        result:json

    method:listTemplates
        """
        list ays templates
        """
        var:repo_path str,,services in that base path will only be returned otherwise all paths @tags: optional
        result:list

    method:listBlueprints
        """
        list all blueprints
        """
        var:repo_path str,,blueprints in that base path will only be returned otherwise all paths @tags: optional
        result:json
    method:findServices
        """
        Search for some services
        """
        var:repo_path str,,will look in this repo
        var:role str,,role of the service @tags:optional
        var:templatename str,,name of the template of the service @tags:optional
        var instante str,,instance name of the requested service
        result:json

    method:reload
        """
        Unload all services from memory and force reload.
        """
        result:json
