##from ActorsLoaderRemote import ActorsLoaderRemote
from JumpScale.portal.portal import PortalServer
#from .PortalServer import PortalServer
#from .PortalClient import PortalClient
#from .PortalClient2 import Resource
import time
#from ActorLoaderLocal import *


from JumpScale import j


class Group():
    pass

class PortalFactory():

    def __init__(self):
        self.__jslocation__ = "j.portal.server"
        # self._inited = False
        self.active = None
        self.inprocess = False

    def get(self):
        return PortalServer.PortalServer()

    def getPortalConfig(self, appname):
        cfg = j.sal.fs.joinPaths(j.dirs.base, 'apps', appname, 'cfg', 'portal')
        return j.config.getConfig(cfg)

    def loadActorsInProcess(self, name='main'):
        """
        make sure all actors are loaded on j.apps...
        """
        class FakeServer(object):
            def __init__(self):
                self.actors = dict()
                try:
                    self.osis = j.clients.osis.getByInstance('main')
                except Exception as e:
                    self.osis = None
                self.epoch = time.time()
                self.actorsloader = j.portalloader.getActorsLoader()
                self.spacesloader = j.portalloader.getSpacesLoader()

            def addRoute(self, *args, **kwargs):
                pass

            def addSchedule1MinPeriod(self, *args, **kwargs):
                pass

            addSchedule15MinPeriod = addSchedule1MinPeriod

        self.inprocess = True
        # self._inited = False
        j.apps = Group()
        basedir = j.sal.fs.joinPaths(j.dirs.base, 'apps', 'portals', name)
        ini = j.tools.inifile.open("%s/cfg/portal.cfg" % basedir)
        appdir = ini.getValue("main", "appdir")
        appdir=appdir.replace("$base",j.dirs.base)
        j.sal.fs.changeDir(appdir)
        server = FakeServer()
        j.portal.server.active = server
        server.actorsloader.scan(appdir)
        server.actorsloader.scan(basedir + "/base")

        for actor in list(server.actorsloader.actors.keys()):
            appname,actorname=actor.split("__",1)
            try:
                server.actorsloader.getActor(appname, actorname)
            except Exception as e:
                print(("*ERROR*: Could not load actor %s %s:\n%s" % (appname,actorname, e)))

