
def main(j, args, params, tags, tasklet):
    docker = args.getTag('docker')
    ayspath = args.getTag('ayspath')

    j.atyourservice.basepath = ayspath
    docker = j.atyourservice.getService(role='docker', instance=docker)

    args.doc.applyTemplate({'data': docker.__dict__})
    params.result = (args.doc, args.doc)
    return params
