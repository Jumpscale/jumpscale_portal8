
def main(j, args, params, tags, tasklet):
    doc = args.doc
    tags = args.tags.tags
    out = "{{kanban: \n"
    yaml = []
    constants = {}
    dynamics = {}

    datatype = tags.pop('kanbandata').strip()
    if datatype == 'issue' or not datatype:
        collection = j.tools.issuemanager.getIssueCollectionFromDB()
    if datatype == 'user':
        collection = j.tools.issuemanager.getUserCollectionFromDB()
    if datatype == 'org' or datatype == 'organization':
        collection = j.tools.issuemanager.getOrgCollectionFromDB()
    if datatype == 'repo' or datatype == 'repository':
        collection = j.tools.issuemanager.getRepoCollectionFromDB()

    def emptyInYaml(result, yaml):
        for result in results:
            result = result.dictFiltered
            yaml += [{'name': result['title'],
                      'content': result['content'],
                      'id': result['id'],
                      'state': 'done' if result['isClosed'] else 'new'}]

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
