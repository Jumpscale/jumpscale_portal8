

def main(j, args, params, tags, tasklet):
    doc = args.doc
    reponame = args.getTag('reponame') or None

    ctx = args.requestContext
    aysactor = j.apps.actorsloader.getActor('system', 'atyourservice')
    client = aysactor.get_client(ctx=ctx)
    if reponame:
        templates = client.listTemplates(repository=reponame).json()
    else:
        templates = client.listAYSTemplates().json()
    try:
        args.doc.applyTemplate({'templates': templates, 'reponame': reponame})
    except Exception as e:
        args.doc.applyTemplate({'error': str(e)})

    params.result = (doc, doc)

    return params
