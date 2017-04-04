from collections import OrderedDict


def main(j, args, params, tags, tasklet):
    try:
        reponame = args.getTag('reponame')
        actors = j.apps.system.atyourservice.listActors(reponame, ctx=args.requestContext)

        if actors:
            args.doc.applyTemplate({'actors': actors, 'reponame': reponame})
        else:
            args.doc.applyTemplate({'error': 'No runs on this repo', 'reponame': reponame})

    except Exception as e:
        args.doc.applyTemplate({'error': e.__str__()})

    params.result = (args.doc, args.doc)
    return params
