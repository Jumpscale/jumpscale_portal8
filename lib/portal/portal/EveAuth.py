from eve.auth import BasicAuth, app


class EveAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        # use Eve's own db driver; no additional connections/resources are used
        users = app.data.driver.db['user']
        lookup = {'name': username}
        if allowed_roles:
            # only retrieve a user if his roles match ``allowed_roles``
            lookup['groups'] = allowed_roles[0]
        user = users.find_one(lookup)
        return user is not None

    def authorized(self, allowed_roles, resource, method):
        from flask import request
        user = request.environ['beaker.session'].get('user')
        if not user:
            return False
        users = app.data.driver.db['user']
        lookup = {'name': user}
        if allowed_roles:
            # only retrieve a user if his roles match ``allowed_roles``
            lookup['groups'] = allowed_roles[0]
        user = users.find_one(lookup)
        return user is not None
