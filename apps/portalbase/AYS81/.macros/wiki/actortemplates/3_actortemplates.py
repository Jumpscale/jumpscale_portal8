

def main(j, args, params, tags, tasklet):
    doc = args.doc
    ayspath = args.getTag('ayspath') or ''
    # if ayspath:
    #     repo = j.atyourservice.repoGet(ayspath)
    #     templates = repo.templates
    # else:
    #     templates = j.atyourservice.actorTemplates
    #templates = j.apps.system.atyourservice.listTemplates()
    #print("<0000000000000000000000000000000", templates)
    if not ayspath:
        reponame = None
    else:
        reponame = j.sal.fs.getBaseName(ayspath)
    out = []
    try:
        templateNames = j.apps.system.atyourservice.listTemplates(reponame)
        templates = []
        for repo in list(templateNames.keys()):
            for template in templateNames[repo]:
                templates.append(j.apps.system.atyourservice.getTemplate(repository=repo, template=template))
        args.doc.applyTemplate({'templates': templates, 'aysrepo': ayspath, 'reponame': reponame})
    except Exception as e:
        args.doc.applyTemplate({'error': str(e)})

    params.result = (doc, doc)

    return params
