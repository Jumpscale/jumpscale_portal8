def main(j, args, params, tags, tasklet):
    guid = args.getTag('guid')
    if not guid:
        out = 'Missing GUID'
        params.result = (out, args.doc)
        return params

    user = j.apps.system.usermanager.userget('', guid=guid)
    if not user:
        out = 'Could not find Username: %s' % guid
        params.result = (out, args.doc)
        return params

    obj = user.dump()
    obj['breadcrumbname'] = obj['id']
    args.doc.applyTemplate(obj)
    params.result = (args.doc, args.doc)
    return params
