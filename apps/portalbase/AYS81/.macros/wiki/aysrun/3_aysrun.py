

def main(j, args, params, tags, tasklet):
    arg_repo = args.getTag('repo')
    arg_runid = args.getTag('runid')

    repo = j.atyourservice.repoGet(arg_repo)
    run = repo.runGet(key=arg_runid)

    if run:
        args.doc.applyTemplate({'run': run, 'data': run.model.dictFiltered, 'reponame': repo.name})
    else:
        args.doc.applyTemplate({'error': 'No run found'})

    params.result = (args.doc, args.doc)
    return params
