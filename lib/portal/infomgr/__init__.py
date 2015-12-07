from JumpScale import j


def cb():
    from .InfoMgr import InfoMgr
    return InfoMgr

j.base.loader.makeAvailable(j, 'tools')
j.tools._register('infomgr', cb)
