from JumpScale import j


def cb():
    from .DataTables import DataTables
    return DataTables

j.base.loader.makeAvailable(j, 'tools')
j.tools._register('datatables', cb)
