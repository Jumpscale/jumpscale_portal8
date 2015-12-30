def main(j, args, params, tags, tasklet):
    import yaml
    import ujson as json
    import datetime

    id = args.getTag('id')
    audit_model = j.data.models.Audit

    if not id:
        out = "No ID given for audit"
        params.result = (out, args.doc)
        return params

    audit = j.data.models.get(audit_model,guid=id)
    for key in ('kwargs', 'args', 'result'):
        audit[key] = yaml.dump(json.loads(audit[key])).replace("!!python/unicode ", "")


    audit['time'] = datetime.datetime.fromtimestamp(audit['timestamp']).strftime('%m-%d %H:%M:%S') or 'N/A'

    args.doc.applyTemplate(audit)
    params.result = (args.doc, args.doc)
    return params
