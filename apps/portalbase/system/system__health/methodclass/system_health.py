from JumpScale import j

class system_health(j.tools.code.classGetBase()):

    """
    Alerts handler
    
    """

    def __init__(self):
        self.scl = j.clients.osis.getNamespace('system', j.core.portal.active.osis)
        self.acl = j.clients.agentcontroller.get()


    def run(self, nid=None, **kwargs):
        if nid:
            nid = int(nid)
            j.core.grid.healthchecker.runAllOnNode(nid, False)
        else:
            j.core.grid.healthchecker.runOnAllNodes(False)
        return "Scheduled healthcheck"

