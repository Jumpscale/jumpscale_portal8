from JumpScale import j


class PortalAuthenticatorMongoEngine(object):

    def __init__(self):
        self.usermodel = j.data.models.User
        self.groupmodel = j.data.models.Group
        self.key2user = {user['authkey']: user['guid'] for user in j.data.models.User.find( query={'authkey': {'$ne': ''}}, redis=False)}

    def getUserFromKey(self, key):
        if key not in self.key2user:
            return "guest"
        return self.key2user[key]

    def _getkey(self, model, name):
        results = model.find({'name': name})
        if results:
            return results[0]['guid']
        else:
            return "%s_%s" % (j.application.whoAmI.gid, name)

    def getUserInfo(self, user):
        return j.data.models.get(self.usermodel, self._getkey(self.usermodel, user), redis=False)

    def getGroupInfo(self, groupname):
        return j.data.models.get(self.groupmodel, self._getkey(self.groupmodel, groupname), redis=False)

    def userExists(self, user):
        return j.data.models.get(self.usermodel, self._getkey(self.usermodel, user), redis=False)

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
        return self.usermodel.find({})

    def listGroups(self):
        return self.groupmodel.find({})

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
        result = j.data.models.authenticate(username=login, passwd=passwd)
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
