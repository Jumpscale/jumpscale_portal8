from collections import OrderedDict


def main(j, args, params, tags, tasklet):
    name = args.getTag('aysname')
    ayspath = args.getTag('ayspath') or None

    template = j.apps.system.atyourservice.listTemplates(repo_path=ayspath)[ayspath][name]
    info = {}
    instances = []
    for key, value in template.__dict__.items():
        if key.startswith('_'):
            continue
        info[key] = value.replace('|', '\|')

    for ayspath, services in j.apps.system.atyourservice.listServices(repo_path=ayspath, role=name).items():
        for service in services.values():
            service_instance = service.instance
            instances.append('[%s|cockpit/AYSInstance?shortkey=%s&ayspath=%s]' % (service_instance, service, ayspath))

    info = OrderedDict(sorted(info.items()))
    args.doc.applyTemplate({'data': info, 'instances': instances})
    params.result = (args.doc, args.doc)
    return params
