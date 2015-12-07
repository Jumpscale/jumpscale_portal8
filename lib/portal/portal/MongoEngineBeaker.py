from beaker.container import NamespaceManager
from JumpScale import j


class MongoEngineBeaker(NamespaceManager):
    def __init__(self, id, namespace_args, **kwargs):
        self._client = j.core.models.getSessionCacheModel()

    def __getitem__(self, key):
        item = j.core.models.get(self._client._class_name, key)
        if item:
            return item
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        if 'user' not in value:
            self._remove(key)
            return
        elif value['user'] == 'guest':
            return
        sessioncache = self._client()
        sessioncache.value = value
        sessioncache.save()

    def _remove(self, key):
        j.core.models.remove(self._client._class_name, key)

    def __contains__(self, key):
        key = "%s_%s" % (self.namespace, key)
        return self._client.exists(self._namespace, self._category, key)

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
