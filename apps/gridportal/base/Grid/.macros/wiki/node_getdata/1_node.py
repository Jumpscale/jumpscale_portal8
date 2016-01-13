
try:
    import ujson as json
except:
    import json
def main(j, args, params, tags, tasklet):

    #macro puts obj info as params on doc, when show used as label, shows the content of the obj in nicely structured code block
    nid = args.getTag('nid')
    gid = args.getTag('gid')
    guid = args.getTag('guid')
    if not nid or not gid:
        params.result = ('Node "nid" and "gid" must be passed.', args.doc)
        return params
    gid = int(gid)
    nid = int(nid)

    node = {}

    if j.data.models.system.Node.find({'gid':gid,'nid':nid}):
        node = j.data.models.system.Node.find({'gid':gid,'nid':nid})[0].to_dict()
    grid = {'name': 'N/A'}
    if j.data.models.system.Grid.find({'gid':gid}):
        grid = j.data.models.system.Grid.find({'gid':gid})[0]
    if not node:
        params.result = ('Node with and id %s_%s not found' % (gid, nid), args.doc)
        return params

    #obj is a dict
    node["ipaddr"]=", ".join(node["ipaddr"])
    node["roles"]=", ".join(node["roles"])

    r=""
    for netitem in node["netaddr"]:
        dev = netitem['name']
        ip = netitem['ip']
        mac = netitem['mac']
        r+="|%-15s | %-20s | %s| \n"%(dev,mac,ip)

    node["netaddr"]=r
    node['gridname'] = grid['name']
    node['nodename'] = node['name']

    args.doc.applyTemplate(node)
    params.result = (args.doc, args.doc)
    return params


def match(j, args, params, tags, tasklet):
    return True


