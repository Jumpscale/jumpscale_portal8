
def main(j, args, params, tags, tasklet):
    shortkey = args.getTag('shortkey')
    ayspath = args.getTag('ayspath')

    j.atyourservice.basepath = ayspath
    service = j.atyourservice.services[shortkey]
    args.doc.applyTemplate({'data': service.hrd.getHRDAsDict()})
    params.result = (args.doc, args.doc)
    return params
