
def main(j, args, params, tags, tasklet):
    doc = args.doc

    out = list()
    for tree in j.sal.fs.listFilesInDir(j.sal.fs.joinPaths(j.dirs.varDir, 'servicetrees')):
        ayspath = j.sal.fs.getBaseName(tree.rsplit('.json', 1)[0]).replace('__', '/')
        j.atyourservice.basepath = ayspath
        services = j.atyourservice.services
        out.append('h3. Services under %s' % ayspath)
        out.append('||Domain||Name||Instance||')
        for _, service in services.items():
            out.append('|%s|%s|[%s|cockpit/AYSInstance?shortkey=%s&ayspath=%s]|' % (service.domain, service.name,
                                                                                 service.instance, service.shortkey, ayspath))
    out = '\n'.join(out)
    params.result = (out, doc)

    return params
