from collections import OrderedDict


def main(j, args, params, tags, tasklet):
    shortkey = args.getTag('shortkey')
    ayspath = args.getTag('ayspath')

    j.atyourservice.basepath = ayspath
    service = j.atyourservice.services[shortkey]
    obj = service.hrd.getHRDAsDict()
    del obj['service.name']

    hidden = ['key.priv', 'password', 'passwd', 'pwd']
    for key in list(set(obj.keys()) & set(hidden)):
        obj[key] = '**VALUE HIDDEN**'

    for key, value in service.producers.items():
        producer = 'producer.%s' % key
        producer_name = value[0]
        obj[producer] = ('[%s|cockpit/AYSInstance?shortkey=%s&ayspath=%s]' % (producer_name.instance, producer_name, ayspath))

    if service.parent:
        parent = service.parent
        service.parents.remove(parent)
        obj['parent'] = ('[%s|cockpit/AYSInstance?shortkey=%s&ayspath=%s]' % (parent.instance, parent, ayspath))

    parents = service.parents
    if parents:
        obj['parents'] = list()
        for parent in parents:
            obj['parents'].append(('[%s|cockpit/AYSInstance?shortkey=%s&ayspath=%s]' % (parent.instance, parent, ayspath)))

        obj['parents'] = ', '.join(obj['parents'])
    link_to_template = ('[%s|cockpit/AYSTemplate?aysdomain=%s&aysname=%s]' % (service.name,
                                                                              service.domain, service.name))
    obj = OrderedDict(sorted(obj.items()))

    args.doc.applyTemplate({'data': obj, 'type': link_to_template, 'instance': service.instance, 'state': service.state})
    params.result = (args.doc, args.doc)
    return params
