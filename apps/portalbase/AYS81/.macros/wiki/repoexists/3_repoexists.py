from collections import OrderedDict


def main(j, args, params, tags, tasklet):
    try:
        reponame = args.getTag('reponame')
        ctx = args.requestContext
        aysactor = j.apps.actorsloader.getActor('system', 'atyourservice')
        client = aysactor.get_client(ctx=ctx)
        repo = client.getRepository(reponame)
        if not repo:
            raise NotFoundException("repo does not exist")
        args.doc.applyTemplate({})
    except Exception as e:
        args.doc.applyTemplate({'error': e.__str__()})

    params.result = (args.doc, args.doc)
    return params
