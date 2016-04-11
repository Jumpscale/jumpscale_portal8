from collections import OrderedDict

def main(j, args, params, tags, tasklet):
    docker = args.getTag('docker')
    ayspath = args.getTag('ayspath')

    j.atyourservice.basepath = ayspath
    docker = j.atyourservice.getService(role='node', instance=docker)


    link = ('[%s|cockpit/AYSInstance?shortkey=%s&ayspath=%s]' %(docker.instance,docker.key,ayspath))
    link_to_dockerhost =  ('[%s|/cockpit/dockerhost?ayspath=%s&dockerhost=%s]' % (docker.parent.instance,ayspath, docker.parent.instance))
    args.doc.applyTemplate({'link': link, 'state': docker.state, 'executor': docker.executor.id,'ports': docker.getTCPPorts(), 'parent': link_to_dockerhost})
    params.result = (args.doc, args.doc)
    return params
