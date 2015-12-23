from JumpScale import j


class PortalAuthenticatorMongoEngine(object):

    def __init__(self):
        self.usermodel = j.core.models.getUserModel()
        self.groupmodel = j.core.models.getGroupModel()
        self.key2user = {user['authkey']: user['id'] for user in j.core.models.find(self.usermodel, query={'authkey': {'$ne': ''}})}

    def getUserFromKey(self, key):
        if key not in self.key2user:
            return "guest"
        return self.key2user[key]

    def _getkey(self, model, name):
        print (j.application.whoAmI.gid)
        results = j.core.models.find(model, query={'name': name})
        print (results)
        if results:
            return results[0]['guid']
        else:
            return "%s_%s" % (j.application.whoAmI.gid, name)

    def getUserInfo(self, user):
        return j.core.models.get(self.usermodel, self._getkey(self.usermodel, user))

    def getGroupInfo(self, groupname):
        return j.core.models.get(self.groupmodel, self._getkey(self.groupmodel, groupname))

    def userExists(self, user):
        return j.core.models.get(self.usermodel, self._getkey(self.usermodel, user))

    def createUser(self, username, password, email, groups, domain):
        user = self.usermodel()
        user.name= username
        if isinstance(groups, str):
            groups = [groups]
        user.groups = groups
        if isinstance(email, str):
            email = [email]
        user.emails = email
        user.domain = domain
        user.passwd = j.tools.hash.md5_string(password)
        return user.save()

    def listUsers(self):
        return j.core.models.find(self.usermodel, {})

    def listGroups(self):
        return j.core.models.find(self.groupmodel, {})

    def getGroups(self, user):
        try:
            userinfo = self.getUserInfo(user)
            return userinfo['groups'] + ["all"]
        except:
            return ["guest", "guests"]

    def loadFromLocalConfig(self):
        #@tddo load from users.cfg & populate in osis
        #see jsuser for example
        pass

    def authenticate(self, login, passwd):
        """
        """
        login = login[0] if isinstance(login, list) else login
        passwd = passwd[0] if isinstance(passwd, list) else passwd
        result = j.core.models.authenticate(username=login, passwd=passwd)
        return result

    def getUserSpaceRights(self, username, space, **kwargs):
        spaceobject = kwargs['spaceobject']
        groupsusers = set(self.getGroups(username))

        for groupuser in groupsusers:
            if groupuser in spaceobject.model.acl:
                right = spaceobject.model.acl[groupuser]
                if right == "*":
                    return username, "rwa"
                return username, right

        # No rights .. check guest
        rights = spaceobject.model.acl.get('guest', '')
        return username, rights

    def getUserSpaces(self, username, **kwargs):
        spaceloader = kwargs['spaceloader']
        return [x.model.id.lower() for x in list(spaceloader.spaces.values())]
