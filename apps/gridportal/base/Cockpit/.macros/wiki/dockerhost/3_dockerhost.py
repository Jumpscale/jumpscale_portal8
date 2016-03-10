
def main(j, args, params, tags, tasklet):
    dockerhost = args.getTag('dockerhost')
    ayspath = args.getTag('ayspath')

    j.atyourservice.basepath = ayspath
    dockerhost = j.atyourservice.getService(role='dockerhost', instance=dockerhost)

    args.doc.applyTemplate({'data': dockerhost.__dict__})
    params.result = (args.doc, args.doc)
    return params
