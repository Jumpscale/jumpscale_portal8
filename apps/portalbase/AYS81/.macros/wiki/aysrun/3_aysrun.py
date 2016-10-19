

def main(j, args, params, tags, tasklet):
    arg_repo = args.getTag('repo')
    arg_runid = args.getTag('runid')
    repo = j.atyourservice.repoGet(arg_repo)
    run = repo.runGet(key=arg_runid)
    if run:
        import datetime
        data = run.model.dictFiltered
        data['lastModDate'] = datetime.datetime.fromtimestamp(data['lastModDate']).strftime('%Y-%m-%d %H:%M:%S.%f')
        args.doc.applyTemplate({'run': run, 'data': data, 'reponame': repo.name})
    else:
        args.doc.applyTemplate({'error': 'No run found'})

    params.result = (args.doc, args.doc)
    return params
