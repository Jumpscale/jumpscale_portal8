from collections import OrderedDict



def main(j, args, params, tags, tasklet):
    name = args.getTag('aysname')
    ayspath = args.getTag('ayspath') or None

    repo = j.atyourservice.repoGet(ayspath)
    template = repo.templates.get(name, None) if repo else None

    if template:
        info = {}
        code_bloks = {
            'schema.hrd': template.schemaHrd.content,
            'schema.capnp': template.schemaCapnpText
        }

        services = repo.servicesFind(actor=template.name)
        info = OrderedDict(sorted(info.items()))
        args.doc.applyTemplate({'data': info, 'services': services, 'code_bloks': code_bloks, 'template_name': name})
    else:
        args.doc.applyTemplate({'error': 'template does not exist'})

    params.result = (args.doc, args.doc)
    return params
