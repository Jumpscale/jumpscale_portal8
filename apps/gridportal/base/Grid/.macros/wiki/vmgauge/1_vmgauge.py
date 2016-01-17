def main(j, args, params, tags, tasklet):
    doc = args.doc
    id = args.getTag('id')
    width = args.getTag('width')
    height = args.getTag('height')
    result = "{{jgauge width:%(width)s id:%(id)s height:%(height)s val:%(running)s start:0 end:%(total)s}}"
    running = j.data.models.system.Machine.find({'state': 'RUNNING'})
    if not running:
        params.result = ('Could not find a running Machine', args.doc)
        return params

    total = len(j.data.models.system.Machine.find({}))
    result = result % {'height': height,
                       'width': width,
                       'running': running,
                       'id': id,
                       'total': total}
    params.result = (result, doc)
    return params
