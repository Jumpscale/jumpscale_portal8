def main(j, args, params, tags, tasklet):
    guid = args.getTag('guid')
    if not guid:
        out = 'Missing GUID'
        params.result = (out, args.doc)
        return params

    group = j.apps.system.usermanager.modelGroup.get(guid)
    if not group:
        out = 'Could not find Group: %s' % guid
        params.result = (out, args.doc)
        return params

    obj = group.dump()
    obj['breadcrumbname'] = obj['id']
    args.doc.applyTemplate(obj)
    params.result = (args.doc, args.doc)
    return params
