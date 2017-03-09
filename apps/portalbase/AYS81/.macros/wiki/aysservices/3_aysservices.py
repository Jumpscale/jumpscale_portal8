

def main(j, args, params, tags, tasklet):
    try:
        doc = args.doc
        ayspath = args.getTag('ayspath') or ''
        reponame = args.getTag('reponame') or ''
        # actor = j.apps.actorsloader.getActor("ays81", "atyourservice")
        # for _, services in actor.listServices(ayspath, ctx=args.requestContext).items():
            # out.extend(services)
        services = j.apps.system.atyourservice.listServices(reponame)
        services = services[reponame]
        args.doc.applyTemplate({'services': services, 'reponame': reponame})
    except Exception as e:
        args.doc.applyTemplate({'error': str(e)})

    params.result = (args.doc, args.doc)

    return params
