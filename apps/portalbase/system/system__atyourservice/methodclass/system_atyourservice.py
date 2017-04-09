from JumpScale import j
from JumpScale.portal.portal import exceptions
from collections import OrderedDict
import requests
import json
import jwt


class system_atyourservice(j.tools.code.classGetBase()):

    """
    gateway to atyourservice
    """

    def __init__(self):
        self.cuisine = j.tools.cuisine.local

    def get_client(self, **kwargs):
        ctx = kwargs['ctx']
        cfg = j.application.instanceconfig
        production = False
        try:
            cl = j.clients.atyourservice.get()
        except:
            raise exceptions.ServiceUnavailable("AYS server isn't available.")

        if isinstance(cfg, dict):
            # need to upgrade config
            production = cfg.get('production', False)
        if production:
            oauth_ctx = ctx.env['beaker.session'].get('oauth', None)
            if oauth_ctx is None:
                raise exceptions.BadRequest("No oauth information in session")

            access_token = oauth_ctx.get('access_token', None)
            if access_token is None:
                raise exceptions.BadRequest("No access_token in session")
            cl.api.set_auth_header('bearer ' + access_token)

        return cl.api.ays

    def createRun(self, repository=None, **kwargs):
        """
        get run
        param:repository
        param: runid
        result json of runinfo
        """
        cl = self.get_client(**kwargs)
        aysrun = cl.createRun(data=None, repository=repository).json()
        return aysrun['key']

    def templatesUpdate(self, repo=None, template_name=None, ays_repo=None, **kwargs):
        cl = self.get_client(**kwargs)
        if not repo and not template_name:
            if not ays_repo:
                updated = list()
                for domain, domain_info in j.atyourservice.config['metadata'].items():
                    base, provider, account, repo, dest, url = j.do.getGitRepoArgs(domain_info.get('url'),
                                                                                   codeDir=j.dirs.CODEDIR)
                    self.cuisine.development.git.pullRepo(domain_info.get('url'),
                                                           branch=domain_info.get('branch', 'master'),
                                                           dest=dest)
                    updated.append(domain)
                return "template repos [" + ', '.join(updated) + "] are updated"
            else:
                updated = self.cuisine.development.git.pullRepo(ays_repo, codedir=j.dirs.CODEDIR)
                return "template %s repo updated" % updated
        elif not template_name:
            cl.updateTemplates(repo)
            return "templates updated"
        cl.updateTemplate(repo, template_name)
        return "template updated"

    def addTemplateRepo(self, url, branch='master', **kwargs):
        """
        Add a new service template repository.
        param:url Service template repository URL
        param:branch Branch of the repo to use default:master
        result json
        """
        cl = self.get_client(**kwargs)
        if url == '':
            raise exceptions.BadRequest("URL can't be empty")

        if not url.startswith('http'):
            raise exceptions.BadRequest("URL Format not valid. It should starts with http")

        if url.endswith('.git'):
            url = url[:-len('.git')]

        try:
            data = j.data.serializer.json.dumps(dict(url=url, branch=branch))
            cl.addTemplateRepo(data=data)
        except j.exceptions.RuntimeError as e:
            raise exceptions.BadRequest(e.message)

        return "Repository added"

    def createBlueprint(self, repository, blueprint, contents, **kwargs):
        """
        create a blueprint
        param:repository where blueprint will be created
        param:blueprint blueprint name
        param:contents content of blueprint
        result json
        """
        cl = self.get_client(**kwargs)

        data = j.data.serializer.json.dumps(dict(name=blueprint, content=contents))
        return cl.createNewBlueprint(repository=repository, data=data)

    def deleteBlueprint(self, repository, blueprint, **kwargs):
        """
        delete a blueprint
        param:repository where blueprint will be created
        param:blueprint blueprint name
        result json
        """
        cl = self.get_client(**kwargs)
        return cl.deleteBlueprint(repository, blueprint)

    def executeBlueprint(self, repository, blueprint='', **kwargs):
        """
        execute blueprint
        param:name blueprints in that base name will only be returned otherwise all names
        result json
        """
        cl = self.get_client(**kwargs)
        try:
            cl.executeBlueprint(repository=repository, blueprint=blueprint)
        except Exception as e:
            raise exceptions.BadRequest(str(e))

        msg = "blueprint executed"
        return msg

    def quickBlueprint(self, repository, name='', contents='', **kwargs):
        """
        quickly execute blueprint and remove from filesystem
        param:contents of blueprint
        result jsong
        """
        cl = self.get_client(**kwargs)

        bpname = name or j.data.time.getLocalTimeHRForFilesystem() + '.yaml'
        data = dict(content=contents, name=bpname)
        try:
            cl.createBlueprint(repository=repository, data=data)
            cl.executeBlueprint(data=None, repository=repository, blueprint=bpname)
            if not name:
                cl.archiveBlueprint(data=None, repository=repository, blueprint=bpname)
        except Exception as e:
            raise exceptions.BadRequest("Blueprint failed to execute. Error was %s" % e)
        msg = "Blueprint executed!"
        return msg

    def listBlueprints(self, repository=None, archived=True, **kwargs):
        """
        list all blueprints
        param:name blueprints in that base name will only be returned otherwise all names
        result json
        """
        cl = self.get_client(**kwargs)

        try:
            bps = cl.listBlueprints(repository=repository).json()
            return bps
        except Exception as e:
            raise exceptions.BadRequest(str(e))

    def getBlueprint(self, repository=None, blueprint=None, **kwargs):
        """
        get a Blueprint
        """
        cl = self.get_client(**kwargs)

        try:
            blueprint = cl.getBlueprint(repository=repository, blueprint=blueprint).json()
            return blueprint
        except Exception as e:
            raise exceptions.BadRequest(str(e))

    def archiveBlueprint(self, repository, blueprint, **kwargs):
        """
        archive blueprint
        param:name blueprints in that base name will only be returned otherwise all names
        result json
        """
        cl = self.get_client(**kwargs)

        try:
            cl.archiveBlueprint(blueprint=blueprint, repository=repository)
        except Exception as e:
            raise exceptions.BadRequest(str(e))
        return "blueprint archived."

    def restoreBlueprint(self, repository, blueprint, **kwargs):
        """
        list all blueprints
        param:name blueprints in that base name will only be returned otherwise all names
        result json
        """
        cl = self.get_client(**kwargs)

        try:
            cl.restoreBlueprint(blueprint=blueprint, repository=repository)
        except Exception as e:
            raise exceptions.BadRequest(str(e))
        return "blueprint restored."

    def listTemplates(self, repository=None, **kwargs):
        """
        list all templates of a certain type
        result json
        """
        cl = self.get_client(**kwargs)

        templates = dict()

        repos = []
        if repository is not None:
            repos = [cl.listRepositories().json()]
        else:
            repos = [r['name']for r in repos]

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

        return cl.getTemplate(repository=repository, name=template)

    def listAYSTemplates(self, **kwargs):
        """
        list all ays templates
        """
        cl = self.get_client(**kwargs)

        templates = cl.listAYSTemplates().json()
        return templates

    def getAYSTemplate(self, template, **kwargs):
        """
        get an AYS templates
        """
        cl = self.get_client(**kwargs)

        templates = cl.getAYSTemplate(template).json()
        return templates

    def listActors(self, repository, **kwargs):
        """
        list add instantiated actors in a repo
        """
        cl = self.get_client(**kwargs)

        actors = cl.listActors(repository).json()
        return actors

    def getActorByName(self, repository, name, **kwargs):
        """
        list add instantiated actors in a repo
        """
        cl = self.get_client(**kwargs)

        actor = cl.getActorByName(repository, name).json()
        return actor

    def createRepo(self, name, **kwargs):
        cl = self.get_client(**kwargs)

        git_url = kwargs['git_url']
        data = j.data.serializer.json.dumps({'name': name, "git_url": git_url})
        try:
            resp = cl.createRepository(data=data)
        except Exception as e:
            if "Failed to establish a new connection" in str(e.args[0]):
                raise requests.exceptions.ConnectionError('Ays API server is not running')
            raise RuntimeError("unknown error in creation of repo:%s" % e)
        if resp.status_code != 200:
            ret = resp.json()
            ret['status_code'] = resp.status_code
            return ret
        return resp.json()

    def deleteRepo(self, repository, **kwargs):
        cl = self.get_client(**kwargs)

        try:
            reponame = repository
            cl.deleteRepository(reponame)
        except Exception as e:
            raise exceptions.BadRequest(str(e))
        return "repo destroyed."

    # FIXME: how to get a repo key?
    def deleteRuns(self, repository, **kwargs):
        cl = self.get_client(**kwargs)

        try:
            reponame = repository
            repo = j.atyourservice.repoGet(reponame)
            j.core.jobcontroller.db.runs.delete(repo=repo)
        except Exception as e:
            raise exceptions.BadRequest(str(e))

        return "runs removed."

    def simulate(self, repository, **kwargs):
        """
        get run
        param:repository
        param: runid
        result json of runinfo
        """
        cl = self.get_client(**kwargs)

        aysrun = cl.createRun(repository=repository).json()
        return aysrun

    def deleteService(self, repository, role='', instance='', **kwargs):
        cl = self.get_client(**kwargs)

        try:
            reponame = repository
            cl.deleteServiceByName(name=instance, role=role, repository=reponame)
        except Exception as e:
            raise exceptions.BadRequest(str(e))
        return "Service deleted"

    def commit(self, message, branch='master', push=True, **kwargs):
        cl = self.get_client(**kwargs)

        path = j.sal.fs.joinPaths(j.dirs.CODEDIR, 'ays_cockpit')
        if not j.atyourservice.exist(path=path):
            return "can't find ays repository for cockpit at %s" % path
        repo = j.atyourservice.get(path=path)

        sshkey_service = repo.getService('sshkey', 'main', die=False)
        if sshkey_service is None:
            return "can't find sshkey service"

        sshkey_service.actions.start(service=sshkey_service)

        if message == "" or message is None:
            message = "log changes for cockpit repo"
        gitcl = j.clients.git.get("/opt/code/cockpit")
        if branch != "master":
            gitcl.switchBranch(branch)

        gitcl.commit(message, True)

        if push:
            print("PUSH")
            gitcl.push()

        msg = "repo committed"
        if push:
            msg += ' and pushed'
        return msg
