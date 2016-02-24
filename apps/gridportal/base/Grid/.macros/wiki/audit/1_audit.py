from JumpScale.data.serializers.SerializerUJson import json
import yaml
import datetime

def main(j, args, params, tags, tasklet):

    guid = args.getTag('guid')
    if not id:
        out = "No GUID given for audit"
        params.result = (out, args.doc)
        return params

    audit = j.data.models.system.Audit.get(guid=guid)
    if not audit:
        out = "No audit with guid %s exists" % guid
        params.result = (out, args.doc)
        return params

    audit = audit.to_dict()
    for key in ('kwargs', 'args', 'result'):
        audit[key] = yaml.dump(json.loads(audit[key])).replace("!!python/unicode ", "")

    audit['time'] = datetime.datetime.fromtimestamp(audit['timestamp']).strftime('%m-%d %H:%M:%S') or 'N/A'

    args.doc.applyTemplate(audit)
    params.result = (args.doc, args.doc)
    return params
