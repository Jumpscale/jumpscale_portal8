[actor] @dbtype:mem,fs
    """
    Actor to generate JWT token on itsyou.online
    """
    method:generateJwtToken
        """
        generate an jwt token
        """
        var:scope str,, scope wanted in the jwt token @tags: optional
        var:audience str,, audience wanted in the jwt token @tags: optional
        result:json
