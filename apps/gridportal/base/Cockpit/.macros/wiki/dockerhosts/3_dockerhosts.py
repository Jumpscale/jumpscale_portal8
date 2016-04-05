
def main(j, args, params, tags, tasklet):
    doc = args.doc

    out = list()

    dockerhosts = j.apps.system.atyourservice.listServicesByRole(role='dockerhost')

    if dockerhosts == {None: []}:
        out = 'no Dockerhosts running on this enviroment'
        params.result = (out, args.doc)
        return params

    out.append('||Instance||STATUS||Path||')
    for ayspath, dockerhostinstances in dockerhosts.items():
        repopath = j.clients.git.get(ayspath)
        repopath = '%s/%s' % (repopath.account, repopath.name)
        for dockerhost in dockerhostinstances:
            out.append('|[%s|/cockpit/dockerhost?ayspath=%s&dockerhost=%s]|N/A|%s|' % (dockerhost.instance,
                                                                                       ayspath, dockerhost.instance,
                                                                                       repopath))
    out = '\n'.join(out)
    params.result = (out, doc)

    return params
