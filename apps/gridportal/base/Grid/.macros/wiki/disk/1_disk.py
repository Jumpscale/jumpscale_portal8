    
def main(j, args, params, tags, tasklet):

    guid = args.getTag('guid')
    gid = args.getTag('gid')
    nid = args.getTag('nid')
    if not guid:
        out = 'Missing disk guid param "guid"'
        params.result = (out, args.doc)
        return params

    key = "%s_%s_%s" % (gid, nid, guid)
    disk = j.apps.system.gridmanager.getDisks(gid=gid,nid=nid,guid=guid)
    if not disk:
        params.result = ('Disk with guid %s not found' % guid, args.doc)
        return params

    disk = disk[0].to_dict()
    node = j.apps.system.gridmanager.getNodes(nid=disk['nid'])
    if node:
        node = node[0].to_dict()

    disk['usage'] = 100 - int(100.0 * float(disk['free']) / float(disk['size']))
    disk['dpath'] = disk['path'] # path is reserved variable for path of request
    disk['bpath'] = j.sal.fs.getBaseName(disk['path'])
    disk['name'] = disk['path'].split('/')[-1]
    for attr in ['size', 'free']:
        disk[attr] = "%.2f %siB" % j.data.units.bytes.converToBestUnit(disk[attr], 'M')
    disk['type'] = ', '.join([str(x) for x in disk['type']])
    disk['nodename'] = node['name']

    args.doc.applyTemplate(disk)
    params.result = (args.doc, args.doc)
    return params

def match(j, args, params, tags, tasklet):
    return True
