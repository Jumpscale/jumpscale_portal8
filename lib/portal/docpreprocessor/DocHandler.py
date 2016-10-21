from JumpScale import j

# import re
import os
# import jinja2

from watchdog.events import FileSystemEventHandler
# The default Observer on Linux (InotifyObserver) hangs in the call to `observer.schedule` because the observer uses `threading.Lock`, which is
# monkeypatched by `gevent`. To work around this, I use `PollingObserver`. It's more CPU consuming than `InotifyObserver`, but still better than
# reloading the doc processor
#
#from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver as Observer


class DocHandler(FileSystemEventHandler):

    def __init__(self, doc_processor):
        self.doc_processor = doc_processor
        self._path_to_tasklet_map = {}
        self._reload_tasklets_map()        


    def _reload_tasklets_map(self):
        """
        Reloads the _path_to_tasklet_map dict by scanning the tasklets groups and load the new tasklets/paths
        """
        for macroexecute in (self.doc_processor.macroexecutorPreprocessor,
                             self.doc_processor.macroexecutorWiki, self.doc_processor.macroexecutorPage):
            for groupname, taskletenginegroup in list(macroexecute.taskletsgroup.items()):
                for group, taskletengine in list(taskletenginegroup.taskletEngines.items()):
                    for tasklet in taskletengine.tasklets:
                        self._path_to_tasklet_map[tasklet.path] = (taskletengine, tasklet)
        

    def on_created(self, event):
        print(('Document {} added'.format(event.src_path)))
        path = os.path.dirname(event.src_path)
        pathItem = event.src_path
        docs = []
        if pathItem:
            lastDefaultPath = ""
            if pathItem.endswith('.wiki'):
                lastDefaultPath = os.path.join(self.doc_processor.space_path, '.space', 'default.wiki')
            elif pathItem.endswith('.md'):
                lastDefaultPath = os.path.join(self.doc_processor.space_path, '.space', 'default.md')
            elif pathItem.endswith('.py'):
                self.reloadMacro(event)
            self.doc_processor.add_doc(pathItem, path, docs=docs, lastDefaultPath=lastDefaultPath)
            self.doc_processor.docs[-1].loadFromDisk()
            self.doc_processor.docs[-1].preprocess()

    def on_modified(self, event):
        print("[DocHandler] Doc [%s] has been modified" % event.src_path)
        # if the file modified is a wiki/md then mark the doc as dirty
        filename = j.sal.fs.getBaseName(event_src)
        docname, ext = os.path.splitext(filename)
        if ext in ('md', 'wiki'):
            # check if the changed file is the default one or a template file, then we need to mark all docs in the space as dirty
            space_path = os.path.join(self.doc_processor.space_path, '.space')
            if space_path in event.src_path:
                for doc in self.doc_processor.name2doc.values():
                    doc.dirty = True
            else:
                doc = self.doc_processor.name2doc.get(docname)
                if doc:
                    doc.dirty = True
        if event.src_path and not event.is_directory and event.src_path.endswith(".py"):
            self.reloadMacro(event)

    def reloadMacro(self, event):
        if event.src_path not in self._path_to_tasklet_map:
            self._reload_tasklets_map()
            if event.src_path in self._path_to_tasklet_map:
                taskletengine, tasklet = self._path_to_tasklet_map[event.src_path]
                taskletengine.reloadTasklet(tasklet)


    on_moved = on_created
