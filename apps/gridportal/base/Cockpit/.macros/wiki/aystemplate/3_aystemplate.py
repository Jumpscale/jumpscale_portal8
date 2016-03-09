
def main(j, args, params, tags, tasklet):
    domain = args.getTag('aysdomain')
    name = args.getTag('aysname')

    template = j.atyourservice.getTemplate(domain=domain, name=name)
    info = {}
    for key, value in template.__dict__.items():
        if key.startswith('_'):
            continue
        info[key] = value.replace('|', '\|')
    args.doc.applyTemplate({'data': info})
    params.result = (args.doc, args.doc)
    return params
