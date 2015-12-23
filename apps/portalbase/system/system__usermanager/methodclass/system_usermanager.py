from JumpScale import j
from JumpScale.portal.portal import exceptions
from JumpScale.portal.portal.auth import auth
import re

class system_usermanager(j.tools.code.classGetBase()):

    """
    register a user (can be done by user itself, no existing key or login/passwd is needed)

    """

    def __init__(self):

        self._te = {}
        self.actorname = "usermanager"
        self.appname = "system"
        self.modelUser = j.core.models.getUserModel()
        self.modelGroup = j.core.models.getGroupModel()

    def authenticate(self, name, secret, **kwargs):
        """
        The function evaluates the provided username and password and returns a session key.
        The session key can be used for doing api requests. E.g this is the authkey parameter in every actor request.
        A session key is only vallid for a limited time.
        param:username username to validate
        param:password password to validate
        result str,,session
        """

        ctx = kwargs['ctx']
        if j.core.portal.active.auth.authenticate(name, secret):
            session = ctx.env['beaker.get_session']()  # create new session
            session['user'] = name
            session.save()
            return session.id
        raise exceptions.Unauthorized("Unauthorized")

    @auth(['admin'])
    def userget(self, name, **kwargs):
        """
        get a user
        param:name name of user
        """
        #return self.modelUser.get("%s_%s"%(j.application.whoAmI.gid,name))
        return j.core.models.find(self.modelUser, {"name": name,"gid":j.application.whoAmI.gid})[0]


    def usergroupsget(self, user, **args):
        """
        return list of groups in which user is member of
        param:user name of user
        result list(str)

        """
        raise NotImplementedError("not implemented method getusergroups")
        user = self._getUser(user)

        if user == None:
            # did not find user
            result = []
        else:
            # print "usergroups:%s" % user.groups
            result = user.groups

        return result

    def _getUser(self, user):
        #users = self.modelUser.find({'id': user})[1:]
        import ipdb; ipdb.set_trace()

        users = j.core.models.find(self.modelUser, {"name": user,"gid":j.application.whoAmI.gid})
        if not users:
            return None
        #return self.modelUser.get(users[0]['guid'])
        return users[0]

    @auth(['admin'])
    def editUser(self, username, groups, emails, domain, password, **kwargs):
        ctx = kwargs['ctx']
        user = self._getUser(username)
        if not user:
            ctx.start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return "User %s not found" % username
        if groups:
            if isinstance(groups, str):
                groups = [x.strip() for x in groups.split(',')]
            elif not isinstance(groups, list):
                ctx.start_response('400 Bad Request', [('Content-Type', 'text/plain')])
                return "Groups paramter should be a list or string"
        else:
            groups = []
        if emails:
            if isinstance(emails, str):
                emails = [x.strip() for x in emails.split(',')]
            elif not isinstance(emails, list):
                ctx.start_resonpnse('400 Bad Request', [('Content-Type', 'text/plain')])
                return "Emails should be a list or a comma seperated string"
            user.emails = emails
        if domain:
            user.domain = domain
        if password:
            user.passwd = j.tools.hash.md5_string(password)

        user.groups = groups
        #self.modelUser.set(user)

        user.save()
        return True

    @auth(['admin'])
    def delete(self, username, **kwargs):
        #self.modelUser.delete(username)

        user = j.core.models.find(self.modelUser, {"name": username})[0]
        self.modelUser.delete(user)
        return True

    @auth(['admin'])
    def deleteGroup(self, id, **kwargs):
        group = j.core.models.find(self.modelGroup, {"name": id})[0]
        self.modelGroup.delete(group)

        #self.modelGroup.delete(id)

    @auth(['admin'])
    def createGroup(self, name, domain, description, **args):
        """
        create a group
        param:name name of group
        param:domain of group
        param:description of group
        result bool

        """
        #if self.modelGroup.find({'id': name})[1:]:
        if j.core.models.find(self.modelGroup, {"name": id})[0]:
            raise exceptions.Conflict("Group with name %s already exists" % name)
        #group = self.modelGroup.new()
        group = self.modelGroup()
        #group.id = name
        group.name = name
        group.domain = domain
        group.description = description
        #self.modelGroup.set(group)
        group.save()
        return True

    @auth(['admin'])
    def editGroup(self, name, domain, description, users, **args):
        """
        edit a group
        param:name name of group
        param:domain of group
        param:description of group
        result bool

        """
        #groups = self.modelGroup.find({'': name})[1:]
        groups =  j.core.models.find(self.modelGroup, {"name": name})

        if not groups:
            raise exceptions.NotFound("Group with name %s does not exists" % name)
        else:
            group = groups[0]
        if users and isinstance(users, str):
            users = users.split(',')
        #group['id'] = name
        group['name'] = name
        group['domain'] = domain
        group['description'] = description
        group['users'] = users
        #self.modelGroup.set(group)
        group.save()
        return True

    def _isValidUserName(self, username):
        r = re.compile('^[a-z0-9]{1,20}$')
        return r.match(username) is not None

    @auth(['admin'])
    def create(self, username, emails, password, groups, domain, **kwargs):
        ctx = kwargs['ctx']
        headers = [('Content-Type', 'text/plain'), ]

        if not self._isValidUserName(username):
            ctx.start_response('409', headers)
            return 'Username may not exceed 20 characters and may only contain a-z and 0-9'

        check, result = self._checkUser(username)
        if check:
            ctx.start_response('409', headers)
            return "Username %s already exists" % username
        groups = groups or []
        return j.core.portal.active.auth.createUser(username, password, emails, groups, None)

    def _checkUser(self, username):

        users = j.core.models.find(self.modelUser, {"name": username})
        #users = self.modelUser.find({'id': username})[1:]
        if not users:
            return False, 'User %s does not exist' % username
        return True, users[0]

    def userexists(self, name, **args):
        """
        param:name name
        result bool

        """
        #return self.modelUser.exists("%s_%s"%(j.application.whoAmI.gid,name))
        user =  j.core.models.find(self.modelUser, {"name": name,"gid":j.application.whoAmI.gid})[0]
        if user:
            return True

    def whoami(self, **kwargs):
        """
        result current user
        """
        ctx = kwargs["ctx"]
        return str(ctx.env['beaker.session']["user"])


    def userregister(self, name, passwd, emails, reference, remarks, config, **args):
        """
        param:name name of user
        param:passwd chosen passwd (will be stored hashed in DB)
        param:emails comma separated list of email addresses
        param:reference reference as used in other application using this API (optional)
        param:remarks free to be used field by client
        param:config free to be used field to store config information e.g. in json or xml format
        result bool

        """
        # put your code here to implement this method
        raise NotImplementedError("not implemented method userregister")