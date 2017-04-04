

def main(j, args, params, tags, tasklet):
    try:
        reponame = args.getTag('reponame')
        runid = args.getTag('runid')
        run = j.apps.system.atyourservice.getRun(reponame, runid, ctx=args.requestContext)
        if run:
            args.doc.applyTemplate({'run': run, 'reponame': reponame})
        else:
            args.doc.applyTemplate({'error': 'No run found'})
    except Exception as e:
        args.doc.applyTemplate({'error': e.__str__()})

    params.result = (args.doc, args.doc)
    return params
