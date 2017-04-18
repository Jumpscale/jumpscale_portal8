

def main(j, args, params, tags, tasklet):
    try:
        # arg_repo = args.getTag('reponame')
        # reponame = j.sal.fs.getBaseName(arg_repo)

        ctx = args.requestContext
        aysactor = j.apps.actorsloader.getActor('system', 'atyourservice')
        client = aysactor.get_client(ctx=ctx)

        reponame = args.getTag('reponame')
        repo = client.getRepository(reponame).json()
        args.doc.applyTemplate({'repo': repo})
        params.result = (args.doc, args.doc)

    except Exception as e:
        args.doc.applyTemplate({'error': e.__str__()})
        params.result = (args.doc, args.doc)
    return params
