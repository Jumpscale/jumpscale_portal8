import datetime

def main(j, args, params, tags, tasklet):
    jid = args.getTag('jid')
    gid = args.getTag('gid')
    nid = args.getTag('nid')

    if not jid or not gid or not nid:
        out = 'Missing ECO params'
        params.result = (out, args.doc)
        return params

    gid = int(gid)
    nid = int(nid)
    try:
        obj = j.data.models.system.Errorcondition.objects.get(__raw__={'jid': jid, 'gid': gid, 'nid': nid}).to_dict()
    except:
        out = 'Could not find Error Condition Object for jid: %s, gid: %s and nid: %s' % (jid, gid, nid)
        params.result = (out, args.doc)
        return params

    obj['epoch'] = "{{div: class=jstimestamp|data-ts=%s}}{{div}}" % obj['epoch']
    obj['lasttime'] = "{{div: class=jstimestamp data-ts=%s}}{{div}}" % obj['lasttime']
    for attr in ['errormessage', 'errormessagePub']:
        obj[attr] = j.html.escape(obj[attr])
    for attr in ['jid']:
        obj['jid'] = '[%(jid)s|job?id=%(jid)s]|' % obj if obj[attr] != 0 else 'N/A'
    obj['guid'] = jid

    args.doc.applyTemplate(obj)
    params.result = (args.doc, args.doc)
    return params
