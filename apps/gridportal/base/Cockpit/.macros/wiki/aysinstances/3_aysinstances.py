
def main(j, args, params, tags, tasklet):
    doc = args.doc

    out = list()
    for ayspath, services in j.apps.system.atyourservice.listServices().items():
        print (ayspath)
        repopath = j.clients.git.get(ayspath)
        repopath = '%s/%s' % (repopath.account, repopath.name)
        out.append('h5. Services under %s' % repopath)
        out.append('||Domain||Name||Instance||')
        for _, service in services.items():
            out.append('|%s|%s|[%s|cockpit/AYSInstance?shortkey=%s&ayspath=%s]|' % (service.domain, service.name,
                                                                                    service.instance, service.shortkey, ayspath))
    out = '\n'.join(out)
    params.result = (out, doc)

    return params
