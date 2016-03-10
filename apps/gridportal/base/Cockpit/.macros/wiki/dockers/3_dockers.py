
def main(j, args, params, tags, tasklet):
    doc = args.doc

    out = list()

    dockerhosts = j.apps.system.atyourservice.listServicesByRole(role='docker')

    out.append('||Instance||STATUS||Path||')
    for ayspath, dockerinstances in dockerhosts.items():
        for docker in dockerinstances:
            out.append('|[%s|/cockpit/docker?ayspath=%s&docker=%s]|N/A|%s|' % (docker.instance,
                                                                               ayspath, docker.instance,
                                                                               docker.path.replace('!', '\!')))
    out = '\n'.join(out)
    params.result = (out, doc)

    return params
