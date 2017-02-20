

def main(j, args, params, tags, tasklet):
    doc = args.doc
    ayspath = args.getTag('ayspath') or None
    templates = j.apps.system.atyourservice.listTemplates(j.sal.fs.getBaseName(ayspath))
    out = []
    try:
        reponame = j.sal.fs.getBaseName(ayspath)
        args.doc.applyTemplate({'templates': list(templates.values()), 'aysrepo': ayspath, 'reponame': reponame})
    except Exception as e:
        args.doc.applyTemplate({'error': str(e)})

    params.result = (doc, doc)

    return params
