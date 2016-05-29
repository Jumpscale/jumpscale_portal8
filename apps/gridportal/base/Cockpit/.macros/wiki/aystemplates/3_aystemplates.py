
def main(j, args, params, tags, tasklet):
    doc = args.doc
    ayspath = args.getTag('ayspath')
    out = list()

    for ayspath, templates in j.apps.system.atyourservice.listTemplates(ayspath).items():
        out.append('h5. AYSRepo: %s' % ayspath)
        out.append('||Name||')

        for template in templates.values():
            out.append('|[%s|cockpit/AYSTemplate?ayspath=%s&aysname=%s]|' % (template.name,
                                                                            ayspath, template.name))
    out = '\n'.join(out)
    params.result = (out, doc)

    return params
