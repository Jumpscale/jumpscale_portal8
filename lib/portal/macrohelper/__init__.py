from JumpScale import j


def cb():
    from .MacroHelper import MacroHelper
    return MacroHelper

j.base.loader.makeAvailable(j, 'tools')
j.tools._register('macrohelper', cb)
