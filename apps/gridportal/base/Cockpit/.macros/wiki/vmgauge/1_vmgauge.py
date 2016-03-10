
def main(j, args, params, tags, tasklet):
    doc = args.doc
    id = args.getTag('id')
    width = args.getTag('width')
    height = args.getTag('height')
    result = "{{jgauge width:%(width)s id:%(id)s height:%(height)s val:%(running)s start:0 end:%(total)s}}"
    running = []
    [running.extend(dockerhosts) for dockerhosts in j.apps.system.atyourservice.listServicesByRole('dockerhost').values()]
    if not running:
        params.result = ('Could not installed dockerhosts', args.doc)
        return params

    total = 45
    result = result % {'height': height,
                       'width': width,
                       'running': len(running),
                       'id': id,
                       'total': total}
    params.result = (result, doc)
    return params
