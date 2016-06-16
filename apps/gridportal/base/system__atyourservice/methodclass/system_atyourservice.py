from JumpScale import j
from JumpScale.portal.portal import exceptions
import jwt


def format_simulate(run):
    out = "Simulation for %s" % run['repository']
    for step in run['steps']:
        out += '%s:\n' % step['action']
        for key in step['services_keys']:
            out += '%s\n' % key
        out += "\n\n"
    return out


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
        self._rest_client = None

    def get_client(self, **kwargs):
        # if client is loaded check the JWT is still valid
        if self._rest_client is not None:
            claims = jwt.decode(self._rest_client._jwt, verify=False)
            # if jwt expire, we fore reloading of client
            # new jwt will be created it needed.
            if j.data.time.epoch >= claims['exp']:
                self._rest_client = None

        if self._rest_client is None:
            ctx = kwargs['ctx']
            username = ctx.env['beaker.session']['user']
            qs = j.data.models.oauth.JWTToken.find({'username': username, 'expire': {'$gt': j.data.time.epoch}})
            if qs.count() <= 0:
                # no JWT token valid in DB, generate a new one.
                token = j.apps.system.oauthtoken.generateJwtToken(scope='', audience='', **kwargs)
            else:
                # JWT available, use this one
                token = qs.first()

            cockpit_cfg = j.portal.server.active.cfg['cockpit']
            base_url = "http://{host}:{port}".format(**cockpit_cfg)
            self._rest_client = j.clients.cockpit.getClient(base_url, token['jwt_token'])
        return self._rest_client

    def listRepos(self, **kwargs):
        cl = self.get_client(**kwargs)
        repos = cl.listRepositories()
        repos = sorted(repos, key=lambda repo: repo['name'])
        return repos

    def listServices(self, repository=None, role=None, templatename=None, **kwargs):
        """
        list all services
        param:name services in that base name will only be returned otherwise all names
        result json of {aysname:services}
        """
        cl = self.get_client(**kwargs)
        output_services = dict()
        repos = self.listRepos()
        repos = [repository] if repository else [r['name']for r in repos]

        for aysrepo in repos:
            services = cl.listServices(repository=aysrepo)
            # repo = j.atyourservice.repos[aysrepo]
            if role:
                output_services.update({aysrepo: {service['key']: service for service in services if service['role'] == role}})
            elif templatename:
                output_services.update({aysrepo: {service['key']: service for service in services if service['name'] == templatename}})
            else:
                output_services.update({aysrepo: services})
        return output_services

    def getService(self, repository, role, instance, **kwargs):
        cl = self.get_client(**kwargs)
        return cl.getServiceByInstance(instance, role, repository)

    def listBlueprints(self, repository=None, **kwargs):
        """
        list all blueprints
        param:name blueprints in that base name will only be returned otherwise all names
        result json
        """
        cl = self.get_client(**kwargs)
        blueprints = dict()
        repos = self.listRepos()
        repos = [repository] if repository else [r['name']for r in repos]

        for aysrepo in repos:
            bps = cl.listBlueprints(repository=aysrepo)
            # repo = j.atyourservice.repos[aysrepo]
            blueprints.update({aysrepo: bps})

        return blueprints

    def listTemplates(self, repository=None, **kwargs):
        """
        list all templates of a certain type
        result json
        """
        cl = self.get_client(**kwargs)
        templates = dict()
        repos = self.listRepos()
        repos = [repository] if repository else [r['name']for r in repos]

        for aysrepo in repos:
            tmpls = cl.listTemplates(repository=aysrepo)
            templates.update({aysrepo: tmpls})
        return templates

    def getTemplate(self, repository, template, **kwargs):
        """
        list all templates of a certain type
        result json
        """
        cl = self.get_client(**kwargs)
        return cl.getTemplate(repository=repository, template=template)

    def createRepo(self, name, **kwargs):
        cl = self.get_client(**kwargs)
        data = j.data.serializer.json.dumps({'name': name})
        resp = cl._client.createNewRepository(data=data)
        if resp.status_code != 200:
            ret = resp.json()
            ret['status_code'] = resp.status_code
            return ret
        return resp.json()

    def deleteRepo(self, repository, **kwargs):
        cl = self.get_client(**kwargs)
        resp = cl._client.deleteRepository(repository=repository)
        if resp.status_code != 204:
            ret = resp.json()
            ret['status_code'] = resp.status_code
            return ret
        return

    def init(self, repository, role='', instance='', force=False, **kwargs):
        cl = self.get_client(**kwargs)
        try:
            resp = cl.initRepository(repository=repository, role=role, instance=instance, force=force)
        except Exception as e:
            raise exceptions.BadRequest(str(e))
        return resp['msg']

    def install(self, repository, role='', instance='', force=False, async=False, **kwargs):
        cl = self.get_client(**kwargs)
        try:
            resp = cl.executeAction(action='install', repository=repository, async=async, force=force)
        except Exception as e:
            raise exceptions.BadRequest(str(e))
        return resp['msg']

    def simulate(self, repository, action, role='', instance='', force=False, **kwargs):
        cl = self.get_client(**kwargs)
        role = '' if not role else role
        instance = '' if not instance else instance
        resp = cl.simulateAction(repository=repository, action=action, role=role, instance=instance, force=force)
        return resp

    def executeAction(self, repository, action, role='', instance='', force=False, async=False, **kwargs):
        cl = self.get_client(**kwargs)
        role = '' if not role else role
        instance = '' if not instance else instance
        try:
            resp = cl.executeAction(repository=repository, action=action, role=role, instance=instance, force=force, async=async)
        except Exception as e:
            raise exceptions.BadRequest(str(e))
        return resp['msg']

    def deleteService(self, repository, role, instance, force=False, **kwargs):
        cl = self.get_client(**kwargs)
        role = '' if not role else role
        instance = '' if not instance else instance
        try:
            resp = cl.deleteServiceByInstance(repository=repository, role=role, instance=instance)
        except Exception as e:
            raise exceptions.BadRequest(str(e))
        return "Service deleted"

    def commit(self, name, **kwargs):
        pass

    def reload(self, **kwargs):
        cl = self.get_client(**kwargs)
        cl.reloadAll()
        return 'service reloaded'
