

def main(j, args, params, tags, tasklet):
    try:
        doc = args.doc
        ayspath = args.getTag('ayspath') or ''
        if ayspath:
            repo = j.atyourservice.repoGet(ayspath)
            templates = repo.templates
        else:
            templates = j.atyourservice.actorTemplates
        out = []
        reponame = j.sal.fs.getBaseName(ayspath)
        args.doc.applyTemplate({'templates': list(templates.values()), 'aysrepo': ayspath, 'reponame': reponame})
    except Exception as e:
        args.doc.applyTemplate({'error': str(e)})

    params.result = (doc, doc)

    return params
