import datetime
import time

def main(j, args, params, tags, tasklet):
    doc = args.doc
    id = args.getTag('id')
    width = args.getTag('width')
    height = args.getTag('height')
    result = "{{jgauge width:%(width)s id:%(id)s height:%(height)s val:%(last24h)s start:0 end:%(total)s}}"
    now = datetime.datetime.now()
    aweekago = j.data.time.getEpochAgo('-7d')
    query = {'epoch': {'eq':'gt', 'value': aweekago, 'name': 'epoch'}}
    firsteco = j.data.models.system.Errorcondition.find(query)
    total = len(firsteco)

    last24h = j.data.time.getEpochAgo('-1d')
    query = {'epoch': {'eq':'gt', 'value': last24h, 'name': 'epoch'}}
    current= len(j.data.models.system.Errorcondition.find(query))
    average = total

    if firsteco:
        date = datetime.datetime.fromtimestamp(firsteco[0]['epoch'])
        delta = now - date
        if delta.days != 0:
            average = int(total / delta.days) * 2

    if average < current:
        average = current

    result = result % {'height': height,
                       'width': width,
                       'id': id,
                       'last24h': current,
                       'total': average}
    params.result = (result, doc)
    return params

def match(j, args, params, tags, tasklet):
    return True
