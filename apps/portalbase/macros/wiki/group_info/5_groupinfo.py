def main(j, args, params, tags, tasklet):
    guid = args.getTag('guid')
    if not guid:
        out = 'Missing GUID'
        params.result = (out, args.doc)
        return params

    group = j.data.models.system.Group.get(guid).to_dict()
    if not group:
        out = 'Could not find Group: %s' % guid
        params.result = (out, args.doc)
        return params

    obj = group
    args.doc.applyTemplate(obj)
    params.result = (args.doc, args.doc)

    return params

