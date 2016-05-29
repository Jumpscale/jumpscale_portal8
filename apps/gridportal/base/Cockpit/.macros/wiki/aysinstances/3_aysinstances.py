
def main(j, args, params, tags, tasklet):
    doc = args.doc
    ayspath = args.getTag('ayspath')

    out = list()
    out.append('||Role||Instance||')
    for ayspath, services in j.apps.system.atyourservice.listServices(ayspath).items():
        for service in services.values():
            out.append('|%s|[%s|cockpit/AYSInstance?shortkey=%s&ayspath=%s]|' % (service.role,
                                                                                 service.instance,
                                                                                 service.key,
                                                                                 ayspath))
    out = '\n'.join(out)
    params.result = (out, doc)

    return params
