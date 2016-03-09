
def main(j, args, params, tags, tasklet):
    doc = args.doc

    out = list()

    dockerhosts = dict()
    for tree in j.sal.fs.listFilesInDir(j.sal.fs.joinPaths(j.dirs.varDir, 'servicetrees')):
        ayspath = j.sal.fs.getBaseName(tree.rsplit('.json', 1)[0]).replace('__', '/')
        j.atyourservice.basepath = ayspath
        services = j.atyourservice.services
        dockerhosts = {service: ayspath for servicekey, service in services.items() if 'dockerhost' in servicekey}

    out.append('||Instance||STATUS||Path||')
    for dockerhost, ayspath in dockerhosts.items():
        dockerhostkey = dockerhost.key.replace('|', '\|')
        out.append('|[%s|/cockpit/dockerhost?ayspath=%s&dockerhost=%s]|N/A|%s|' % (dockerhost.instance,
                                                                                   ayspath, dockerhost.instance,
                                                                                   dockerhost.path))
    out = '\n'.join(out)
    params.result = (out, doc)

    return params
