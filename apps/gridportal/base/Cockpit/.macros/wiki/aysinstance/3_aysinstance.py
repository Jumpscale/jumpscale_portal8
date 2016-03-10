from collections import OrderedDict
def main(j, args, params, tags, tasklet):
    shortkey = args.getTag('shortkey')
    ayspath = args.getTag('ayspath')

    j.atyourservice.basepath = ayspath
    service = j.atyourservice.services[shortkey]
    obj = service.hrd.getHRDAsDict()
    for key,value in service.producers.items():

        producer = 'producer.%s' % key
        producer_name = value[0]
        obj[producer] = ('[%s|cockpit/AYSInstance?shortkey=%s&ayspath=%s]|' % (producer_name.instance, producer_name, ayspath))

    if 'parent' in obj.keys():
        parent = service.parent
        obj['parent'] = ('[%s|cockpit/AYSInstance?shortkey=%s&ayspath=%s]|' % (parent.instance, parent, ayspath))


    if 'service.name' in obj.keys():
        obj['service.name'] = service.instance
        obj['service.template'] = ('[%s|cockpit/AYSTemplate?aysdomain=%s&aysname=%s]|' % (service.name, service.domain,service.name))


    if 'vdc' in obj.keys():
        vdc_instance = obj['vdc']
        vdc_shortkey = 'vdc!%s' % vdc_instance
        obj['vdc'] = ('[%s|cockpit/AYSInstance?shortkey=%s&ayspath=%s]|' % (vdc_instance, vdc_shortkey, ayspath))

    if 'vdcfarm' in obj.keys():
        vdcfarm_instance = obj['vdcfarm']
        vdcfarm_shortkey = 'vdcfarm!%s' % vdcfarm_instance
        obj['vdcfarm'] = ('[%s|cockpit/AYSInstance?shortkey=%s&ayspath=%s]|' % (vdcfarm_instance, vdcfarm_shortkey, ayspath))

    obj = OrderedDict(sorted(obj.items()))
    args.doc.applyTemplate({'data': obj,'name':service.name, 'instance':service.instance})
    params.result = (args.doc, args.doc)
    return params
