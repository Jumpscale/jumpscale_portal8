
def main(j, args, params, tags, tasklet):
    doc = args.doc

    out = list()
    for ayspath, services in j.apps.system.atyourservice.listServices().items():
        out.append('h3. Services under %s' % ayspath)
        out.append('||Domain||Name||Instance||')
        for _, service in services.items():
            out.append('|%s|%s|[%s|cockpit/AYSInstance?shortkey=%s&ayspath=%s]|' % (service.domain, service.name,
                                                                                    service.instance, service.shortkey, ayspath))
    out = '\n'.join(out)
    params.result = (out, doc)

    return params
