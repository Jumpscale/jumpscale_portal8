from beaker.container import NamespaceManager
from JumpScale import j


class MongoEngineBeaker(NamespaceManager):
    def __init__(self, id, namespace_args, **kwargs):
        self.namespace = id

    def __getitem__(self, key):
        item = j.data.models.system.SessionCache.get(guid=self.namespace)
        if item:
            return item.to_dict()
        else:
            raise KeyError(self.namespace)

    def __setitem__(self, key, value):
        if not value.get('user', None):
            self._remove(self.namespace)
            return
        elif value['user'] == 'guest':
            return
        sessioncache = j.data.models.system.SessionCache()
        sessioncache._creation_time = value.get('_creation_time')
        sessioncache._accessed_time = value.get('_accessed_time')
        sessioncache.guid = self.namespace
        sessioncache.user = value.get('user')
        sessioncache.save()

    def _remove(self, key):
        sessioncache = j.data.models.system.SessionCache.get(self.namespace)
        if sessioncache:
            sessioncache.delete()

    def __contains__(self, key):
        key = "%s_%s" % (self.namespace, key)
        return j.data.models.system.SessionCache.exists(key)

    def __delitem__(self, key, **kwargs):
        self._remove(key)

    def acquire_read_lock(self, **kwargs):
        return True

    def release_read_lock(self, **kwargs):
        return True

    def acquire_write_lock(self, **kwargs):
        return True

    def release_write_lock(self, **kwargs):
        return True
