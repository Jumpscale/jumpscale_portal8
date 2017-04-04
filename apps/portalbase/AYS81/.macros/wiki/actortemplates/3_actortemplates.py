

def main(j, args, params, tags, tasklet):
    doc = args.doc
    ayspath = args.getTag('ayspath') or None
    reponame = args.getTag('reponame') or None
    if reponame:
        templates = j.apps.system.atyourservice.listTemplates(repository=reponame, ctx=args.requestContext)[reponame]
    else:
        templates = j.apps.system.atyourservice.listAYSTemplates(ctx=args.requestContext)
    try:
        args.doc.applyTemplate({'templates': templates, 'aysrepo': ayspath, 'reponame': reponame})
    except Exception as e:
        args.doc.applyTemplate({'error': str(e)})

    params.result = (doc, doc)

    return params
