from collections import OrderedDict


def main(j, args, params, tags, tasklet):

    name = args.getTag('aysname')
    ayspath = args.getTag('ayspath') or None
    reponame = args.getTag('reponame') or None

    if not reponame:
        # template = j.atyourservice.actorTemplates[name]
        template = j.apps.system.atyourservice.getAYSTemplate(name)
        services = []
    else:
        template = j.apps.system.atyourservice.getTemplate(reponame, name)
        services = j.apps.system.atyourservice.listServices(repository=reponame, template_name=name)
    if template:
        info = {}
        code_bloks = {
            'action': template['action'],
            'config.yaml': '\n'+j.data.serializer.yaml.dumps(template['config']),
            'schema.capnp': template['schema']
        }
        info = OrderedDict(sorted(info.items()))
        args.doc.applyTemplate({'data': info, 'services': services, 'code_bloks': code_bloks,
                                'template_name': name, 'reponame': j.sal.fs.getBaseName(ayspath) if ayspath else '',
                                'aysrepo': ayspath})
    else:
        args.doc.applyTemplate({'error': 'template does not exist'})

    params.result = (args.doc, args.doc)
    return params
