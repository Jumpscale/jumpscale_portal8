
def main(j, args, params, tags, tasklet):
    doc = args.doc

    out = list()
    dockerhosts = j.apps.system.atyourservice.listServicesByRole(role='docker')

    if dockerhosts == {None: []}:
        out = 'no Dockerhosts running on this enviroment'
        params.result = (out, args.doc)
        return params

    out.append('||Instance||STATUS||Path||')
    for ayspath, dockerinstances in dockerhosts.items():
        repopath = j.clients.git.get(ayspath)
        repopath = '%s/%s' % (repopath.account, repopath.name)
        for docker in dockerinstances:
            out.append('|[%s|/cockpit/docker?ayspath=%s&docker=%s]|N/A|%s|' % (docker.instance,
                                                                               ayspath, docker.instance,
                                                                               repopath))
    out = '\n'.join(out)
    params.result = (out, doc)

    return params
