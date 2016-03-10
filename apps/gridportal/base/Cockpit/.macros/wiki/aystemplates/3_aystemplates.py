
def main(j, args, params, tags, tasklet):
    doc = args.doc

    out = ['||Domain||Name||']
    #for tree in j.sal.fs.listFilesInDir(j.sal.fs.joinPaths(j.dirs.varDir, 'servicetrees')):
    #    ayspath = j.sal.fs.getBaseName(tree.rsplit('.json', 1)[0]).replace('__', '/')
    #    j.atyourservice.basepath = ayspath
    #    services = j.atyourservice.services
    #    out.append('h3. Services under %s' % ayspath)
    #    out.append('||Domain||Name||Instance||')
    #    for _, service in services.items():

    for template in j.apps.system.atyourservice.listTemplates():
        out.append('|%s|[%s|cockpit/AYSTemplate?aysdomain=%s&aysname=%s]|' % (template.domain, template.name,
                                                                        template.domain, template.name))
    out = '\n'.join(out)
    params.result = (out, doc)

    return params
