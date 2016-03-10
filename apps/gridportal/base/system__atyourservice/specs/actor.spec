[actor] @dbtype:mem,fs
    """
    gateway to atyourservice
    """    
    method:listServices
        """
        list all services
        """
        var:path str,,services in that base path will only be returned otherwise all paths @tags: optional
        result:json

    method:listServicesByRole
        """
        list all services of a certain type
        """
        var:role str,, service role
        var:path str,,services in that base path will only be returned otherwise all paths @tags: optional
        result:json

    method:listTemplates
        """
        list ays templates
        """
        result:list

    
