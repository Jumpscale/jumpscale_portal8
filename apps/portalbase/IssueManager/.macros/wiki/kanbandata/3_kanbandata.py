
def main(j, args, params, tags, tasklet):
    doc = args.doc
    tags = args.tags.tags
    out = "{{kanban: \n"
    yaml = []
    constants = {}
    dynamics = {}

    # j.clients.gogs.connectPSQL(ipaddr='127.0.0.1', port=5432, login='gogs', passwd='gogs', dbname='gogs')
    # j.clients.gogs.syncAllFromPSQL(gogsName='gig')

    datatype = tags.pop('kanbandata').strip()
    if datatype == 'issue' or not datatype:
        collection = j.tools.issuemanager.getIssueCollectionFromDB()
    if datatype == 'user':
        collection = j.tools.issuemanager.getUserCollectionFromDB()
    if datatype == 'org' or datatype == 'organization':
        collection = j.tools.issuemanager.getOrgCollectionFromDB()
    if datatype == 'repo' or datatype == 'repository':
        collection = j.tools.issuemanager.getRepoCollectionFromDB()

    user_collection = j.tools.issuemanager.getUserCollectionFromDB()
    repo_collection = j.tools.issuemanager.getRepoCollectionFromDB()

    def emptyInYaml(results, yaml):
        for result in results:
            result = result.dictFiltered
            title_link = '<a href="'+ result['gogsRefs'][0]['url'] + '" target="_blank">' + result["title"] + '</a>'
            data = {'title': title_link,
                    'content': result.get('content', ""),
                    'key': result['key'],
                    'state': 'done' if result['isClosed'] else 'new'}
            if 'assignee' in result:
                data['resourceId'] = result['assignee']
            data['state'] = result['state']
            if data['state'] in ['resolved', 'wontfix']:
                data['state'] = 'closed'
            result['labels'] = result.get('labels', [])
            data['priority'] = result['priority']
            data['tags'] = ",".join(result['labels'])
            yaml += [data]

    if datatype in ['issue']:
        if 'assignees' in tags:
            userid = user_collection.find(name=tags['assignees'])
            if userid:
                userid = userid[0].key
                tags['assignees'] = userid

    for tag, val in tags.items():
        if ',' not in val:
            constants[tag] = val
            continue
        instances = val.split(',')
        for instance in instances:
            dynamics[tag] = instance
            results = collection.find(**dynamics, **constants)
            emptyInYaml(results, yaml)

    if not dynamics:
        results = collection.find(**dynamics, **constants)
        emptyInYaml(results, yaml)

    out += j.data.serializer.yaml.dumps(yaml) + "\n}}"
    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
