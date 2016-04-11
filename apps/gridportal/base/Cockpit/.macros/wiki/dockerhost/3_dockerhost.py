from collections import OrderedDict

def main(j, args, params, tags, tasklet):
    dockerhost = args.getTag('dockerhost')
    ayspath = args.getTag('ayspath')

    j.atyourservice.basepath = ayspath
    dockerhost = j.atyourservice.getService(role='node', instance=dockerhost)

    link = ('[%s|cockpit/AYSInstance?shortkey=%s&ayspath=%s]' % (dockerhost.instance, dockerhost.key, ayspath))
    children = {}
    for key,dockers in dockerhost.listChildren().items():
        for docker in dockers:
            children[key]=('[%s|/cockpit/docker?ayspath=%s&docker=%s]' % (docker,ayspath, docker))


    args.doc.applyTemplate({'state': dockerhost.state, 'link': link, 'children': children,'executor': dockerhost.executor.id})
    params.result = (args.doc, args.doc)
    return params
