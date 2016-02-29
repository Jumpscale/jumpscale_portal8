def main(j, args, params, tags, tasklet):
    import urllib
    guid = args.getTag('guid')
    if not guid:
        out = 'Missing job id param "id"'
        params.result = (out, args.doc)
        return params

    command = j.data.models.system.Command.get(guid=guid)
    if not command:
        params.result = ('Job with id %s not found' % guid, args.doc)
        return params

    obj = command.to_dict()

    obj['node'] = {'name': 'N/A'}
    if obj['nid']:
        node = j.apps.system.gridmanager.getNodes(nid= obj['nid'], gid=obj['gid'])
        if node:
            obj['node'] = node[0]

    obj['roles'] = ', '.join(obj['roles'])
    obj['args'] = j.data.serializer.json.dumps(command.args, indent=2)

    args.doc.applyTemplate(obj)

    params.result = (args.doc, args.doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
