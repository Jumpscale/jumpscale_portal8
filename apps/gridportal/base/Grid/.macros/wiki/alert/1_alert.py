
def main(j, args, params, tags, tasklet):
    guid = args.getTag('guid')
    if not guid:
        out = 'Missing alert param "id"'
        params.result = (out, args.doc)
        return params            

    alert = j.apps.system.gridmanager.getAlerts(guid=guid)
    if not alert:
        params.result = ('Alert with guid %s not found' % guid, args.doc)
        return params

    alert = alert[0].to_dict()

    color = 'green' if alert['state'] in ['RESOLVED', 'CLOSED'] else ('red' if alert['state'] in ['ALERT', 'UNRESOLVED'] else 'orange')
    alert['state'] = '{color:%s}%s{color}' % (color, alert['state'])


    ecos_guid = alert['errorconditions']

    for eco in ecos_guid:
        if not j.data.model.Errorcondition.exists(eco):
            alert['errorconditions'] = None

    args.doc.applyTemplate(alert)

    params.result = (args.doc, args.doc)
    return params