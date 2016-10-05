

def main(j, args, params, tags, tasklet):
    doc = args.doc
    ayspath = args.getTag('ayspath')
    if ayspath:
        repo = j.atyourservice.repoGet(ayspath)
        templates = repo.templates
    else:
        # actor = j.apps.actorsloader.getActor("ays81", "atyourservice")
        templates = j.atyourservice.actorTemplates

    out = []
    try:
        # for template in templates.values():
        args.doc.applyTemplate({'templates': list(templates.values())})
    except Exception as e:
        args.doc.applyTemplate({'error': str(e)})

    params.result = (args.doc, args.doc)

    return params
