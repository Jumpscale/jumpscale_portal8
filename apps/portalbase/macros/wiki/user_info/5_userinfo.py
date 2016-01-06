def main(j, args, params, tags, tasklet):
    guid = args.getTag('guid')
    if not guid:
        out = 'Missing GUID'
        params.result = (out, args.doc)
        return params

    user = j.data.models.User.get(guid=guid).to_dict()
    if not user:
        out = 'Could not find Username: %s' % guid
        params.result = (out, args.doc)
        return params

    obj = user.to_dict()
    obj['breadcrumbname'] = obj['name']
    args.doc.applyTemplate(obj)
    params.result = (args.doc, args.doc)
    return params
