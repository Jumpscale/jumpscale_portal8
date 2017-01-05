

def main(j, args, params, tags, tasklet):
    try:
        arg_repo = args.getTag('repo')
        reponame = j.sal.fs.getBaseName(arg_repo)
        repos = j.atyourservice.reposList()
        repo = None
        for r in repos:
            if reponame == r.name:
                repo = r
                break

        if repo is not None:
            # repo.path = repo.path.replace(j.dirs.CODEDIR, '$codedir')
            # repo.path = repo.path.replace(j.dirs.VARDIR, '$varDir')
            args.doc.applyTemplate({'repo': repo})
            params.result = (args.doc, args.doc)
        else:
            params.result = ("Cant find repository %s" % repo, args.doc)
    except Exception as e:
        args.doc.applyTemplate({'error': e.__str__()})
        params.result = (args.doc, args.doc)
    return params
