import datetime

def main(j, args, params, tags, tasklet):
    guid = args.getTag('guid')
    gid = args.getTag('gid')
    if not guid or not gid:
        out = 'Missing vdisk guid'
        params.result = (out, args.doc)
        return params

    vdisk = j.apps.system.gridmanager.getVDisks(gid=gid, guid=guid)
    if not vdisk:
        params.result = ('VDisk with guid %s not found' % guid, args.doc)
        return params

    def objFetchManipulate(guid):
        obj = vdisk[0].to_dict()
        for attr in ['lastcheck', 'expiration', 'backuptime']:
            value = obj.get(attr)
            if value: 
                obj[attr] = datetime.datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
            else:
                obj[attr] = 'N/A'
        for attr in ['size', 'free', 'sizeondisk']:
            size, unit = j.data.units.bytes.converToBestUnit(obj[attr], 'K')
            if unit:
                unit += "i"
            obj[attr] = "%s %sB" % (size, unit)
        return obj

    push2doc=j.portal.tools.macrohelper.push2doc

    return push2doc(args,params,objFetchManipulate)

def match(j, args, params, tags, tasklet):
    return True
