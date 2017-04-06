from collections import OrderedDict


def main(j, args, params, tags, tasklet):

    name = args.getTag('aysname')
    ayspath = args.getTag('ayspath') or None
    reponame = args.getTag('reponame') or None
    ctx = args.requestContext
    aysactor = j.apps.actorsloader.getActor('system', 'atyourservice')
    client = aysactor.get_client(ctx=ctx)
    if not reponame:
        # FIXME: migrate to ays_api calls if not reponame.
        # template = j.atyourservice.actorTemplates[name]
        template = j.apps.system.atyourservice.getAYSTemplate(name, ctx=args.requestContext)
        services = []
    else:
        template = client.getTemplate(name, reponame).json()
        services = client.listServices(reponame).json()
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
