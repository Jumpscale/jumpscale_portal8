from collections import OrderedDict


def main(j, args, params, tags, tasklet):
    try:
        reponame = args.getTag('reponame')
        runs = j.apps.system.atyourservice.listRuns(reponame, ctx=args.requestContext)[reponame]

        if runs:
            args.doc.applyTemplate({'runs': runs, 'reponame': reponame})
        else:
            args.doc.applyTemplate({'error': 'No runs on this repo', 'reponame': reponame})

    except Exception as e:
        args.doc.applyTemplate({'error': e.__str__()})

    params.result = (args.doc, args.doc)
    return params
