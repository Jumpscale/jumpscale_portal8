from JumpScale import j


def cb():
    from .DefManager import DefManager
    return DefManager

#j.base.loader.makeAvailable(j.core, 'portal')
j.base.loader.makeAvailable(j, 'tools')
j.tools._register('defmanager', cb)
