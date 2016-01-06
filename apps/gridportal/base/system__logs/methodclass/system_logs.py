from JumpScale import j


class system_logs(j.tools.code.classGetBase()):

    def __init__(self):
        self._te = {}
        self.actorname = "logs"
        self.appname = "system"

    def listJobs(self, **args):

        nip = 'localhost'
        if args.get('nip'):
            nip = args.get('nip')
        params = {'ffrom': '', 'to': '', 'nid': '', 'gid': '',
                  'parent': '', 'state': '', 'jsorganization': '', 'jsname': '', 'roles': ''}
        for p in params:
            params[p] = args.get(p)

        if not any(params.values()):
            jobs = j.data.models.system.Job.find({})
        else:
            query = {'query': {'bool': {'must': list()}}}
            if params['ffrom']:
                ffrom = params.pop('ffrom')
                starting = j.data.time.getEpochAgo(ffrom)
                drange = {'range': {'timeStart': {'gte': starting}}}
                query['query']['bool']['must'].append(drange)
            if params['to']:
                to = params.pop('to')
                ending = j.data.time.getEpochAgo(to)
                if query['query']['bool']['must']:
                    query['query']['bool']['must'][0]['range']['timeStart']['lte'] = ending
                else:
                    drange = {'range': {'timeStart': {'lte': ending}}}
                    query['query']['bool']['must'].append(drange)
            if params['roles']:
                roles = params.pop('roles')
                query_string = {"query_string":{"default_field":"roles","query": roles}}
                query['query']['bool']['must'].append(query_string)
            for k, v in params.items():
                if v:
                    if k == 'state':
                        v = v.lower()
                    term = {'term': {k: v}}
                    query['query']['bool']['must'].append(term)

            jobs = j.data.models.system.Job.find(query)

        aaData = list()
        fields = ('jsname', 'jsorganization', 'parent', 'roles', 'state')
        for item in jobs['result']:
            itemdata = list()
            for field in fields:
                itemdata.append(item['_source'].get(field))
            itemargs = j.data.serializer.serializers.ujson.loads(item['_source'].get('args', {}))
            itemdata.append('<a href=%s>%s</a>' % ('/gridlogs/job?jobid=%s' % item['_id'], itemargs.get('msg', '')))
            result = item['_source'].get('result', '{}')
            result = j.data.serializer.serializers.ujson.loads(result if result else '{}')
            itemdata.append(result)
            aaData.append(itemdata)
        return {'aaData': aaData}



    def listNodes(self, **args):
        nodes = j.data.models.system.Node.find({})

        aaData = list()
        fields = ('name', 'roles', 'ipaddr', 'machineguid')
        for node in nodes:
            itemdata = list()
            for field in fields:
                itemdata.append(node[field])
            itemdata.append(node['guid'])
            ipaddr = node['ipaddr'] if node['ipaddr'] else ''
            itemdata.append('<a href="/grid/grid node?nip=%s">link</a>' % ipaddr)
            aaData.append(itemdata)
        return {'aaData': aaData}


    def listECOs(self, **args):
        import JumpScale.baselib.elasticsearch
        esc = j.clients.elasticsearch.get()

        nid = 1
        if args.get('nip'):
            nid = args.get('nid')
        query = {"query":{"bool":{"must":[{"term":{"nid":nid}}]}}}
        ecos = esc.search(query, index='system_eco')

        aaData = list()
        fields = ('appname', 'category', 'epoch', 'errormessage', 'jid', 'level', 'backtrace', 'nid', 'pid')

        for item in ecos['hits']['hits']:
            itemdata = list()
            for field in fields:
                itemdata.append(item['_source'].get(field))
            aaData.append(itemdata)

        if not aaData:
            aaData = [None, None, None, None, None]
        return {'aaData': aaData}


    def listLogs(self, **args):
        import JumpScale.baselib.elasticsearch
        esc = j.clients.elasticsearch.get()

        query = 'null'
        if args.get('nid'):
            nid = args.get('nid')
            query = {"query":{"bool":{"must":[{"term":{"nid":nid}}]}}}

        logs = esc.search(query, index='system_log')

        aaData = list()
        fields = ('appname', 'category', 'epoch', 'message', 'level', 'pid')

        for item in logs['hits']['hits']:
            itemdata = list()
            for field in fields:
                itemdata.append(item['_source'].get(field))
            aaData.append(itemdata)
        return {'aaData': aaData}
