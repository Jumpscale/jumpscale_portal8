
def main(j, args, params, tags, tasklet):
    doc = args.doc

    out = list()
    for tree in j.sal.fs.listFilesInDir(j.sal.fs.joinPaths(j.dirs.varDir, 'servicetrees')):
        ayspath = j.sal.fs.getBaseName(tree.rsplit('.json', 1)[0]).replace('__', '/')
        j.atyourservice.basepath = ayspath
        blueprints = j.atyourservice.blueprints
        for blueprint in blueprints:
            out.append('h5. Blueprint %s' % blueprint.path)
            out.append('{{code:\n%s\n}}' % blueprint.content)
    out = '\n'.join(out)
    params.result = (out, doc)

    return params
