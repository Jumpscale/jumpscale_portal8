
def main(j, args, params, tags, tasklet):
    doc = args.doc
    ayspath = args.getTag('ayspath') or ''
    out = ['||Name||']

    for template in j.apps.system.atyourservice.listTemplates(ayspath)[ayspath].values():
            out.append('|[%s|cockpit/AYSTemplate?ayspath=%s&aysname=%s]|' % (template.name,
                                                                            ayspath, template.name))
    out = '\n'.join(out)
    params.result = (out, doc)

    return params
