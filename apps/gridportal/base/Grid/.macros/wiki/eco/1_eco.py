
import datetime

def main(j, args, params, tags, tasklet):
    guid = args.getTag('guid')


    if not guid:
        out = 'Missing ECO params'
        params.result = (out, args.doc)
        return params

    try:
        obj = j.data.models.system.Errorcondition.objects.get(__raw__={'guid': guid}).to_dict()
    except:
        out = 'Could not find Error Condition Object for guid: %s' % (guid)
        params.result = (out, args.doc)
        return params

    obj['epoch'] = "{{div: class=jstimestamp|data-ts=%s}}{{div}}" % obj['epoch']
    obj['lasttime'] = "{{div: class=jstimestamp data-ts=%s}}{{div}}" % obj['lasttime']
    for attr in ['errormessage', 'errormessagePub']:
        obj[attr] = j.html.escape(obj[attr])
    for attr in ['jid']:
        obj['jid'] = '[%(jid)s|job?id=%(jid)s]|' % obj if obj[attr] != 0 else 'N/A'
    obj['guid'] = guid

    args.doc.applyTemplate(obj)
    params.result = (args.doc, args.doc)
    return params
