import datetime

def main(j, args, params, tags, tasklet):
    guid = args.getTag('id')
    if not guid:
        out = 'Missing NIC guid param "guid"'
        params.result = (out, args.doc)
        return params
    nic = j.data.models.system.Nic.get(guid=guid).to_dict()
    if not nic:
        params.result = ('NIC with guid %s not found' % guid, args.doc)
        return params

    node = j.core.portal.active.osis.get('system', 'node', nic['nid'])
    nic['lastcheck'] = datetime.datetime.fromtimestamp(nic['lastcheck']).strftime('%Y-%m-%d %H:%M:%S')
    nic['ipaddr'] = ', '.join([str(x) for x in nic['ipaddr']])
    nic['nodename'] = node['name']

    args.doc.applyTemplate(nic)
    params.result = (args.doc, args.doc)
    return params

def match(j, args, params, tags, tasklet):
    return True
