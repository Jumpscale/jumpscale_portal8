
def main(j, args, params, tags, tasklet):
    doc = args.doc

    out = list()

    dockerhosts = j.apps.system.atyourservice.listServicesByRole(role='dockerhost')

    out.append('||Instance||STATUS||Path||')
    for ayspath, dockerhostinstances in dockerhosts.items():
        for dockerhost in dockerhostinstances:
            out.append('|[%s|/cockpit/dockerhost?ayspath=%s&dockerhost=%s]|N/A|%s|' % (dockerhost.instance,
                                                                                       ayspath, dockerhost.instance,
                                                                                       dockerhost.path.replace('!', '\!')))
    out = '\n'.join(out)
    params.result = (out, doc)

    return params
