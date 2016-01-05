import datetime

def main(j, args, params, tags, tasklet):
    guid = args.getTag('id')
    if not guid:
        out = 'Missing log guid param "id"'
        params.result = (out, args.doc)
        return params
    log = j.data.models.Log.get(guid=guid)
    if not log:
        params.result = ('Log with guid %s not found' % guid, args.doc)
        return params

    def objFetchManipulate(id):
        for attr in ['epoch']:
            log[attr] = datetime.datetime.fromtimestamp(log[attr]).strftime('%Y-%m-%d %H:%M:%S')
        for attr in ['jid', 'masterjid']:
            log['jid'] = '[%(jid)s|job?id=%(jid)s]|' % log if log[attr] else 'N/A'
        return log.to_dict()
    push2doc=j.tools.macrohelper.push2doc

    return push2doc(args,params,objFetchManipulate)


def match(j, args, params, tags, tasklet):
    return True
