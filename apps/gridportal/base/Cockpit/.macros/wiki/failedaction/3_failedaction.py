
def main(j, args, params, tags, tasklet):
    tags = j.data.tags.getObject(tagstring=args.cmdstr)
    tags = tags.getDict()
    runid = tags.get('runid')
    actionkey = tags.get('actionkey')

    runid = 'actions.%s' % runid
    actionkey = actionkey.replace('___', ' ')
    action = j.actions.actions.get(actionkey)

    if not action:
        params.result = ('Could not find action with runid: "%s" and actionkey: "%s"' % (runid, actionkey), args.doc)
        return params

    action = action.__dict__
    actionadd = dict()
    for key, value in action.items():
        if key == '_parent':
            actionadd['_parentshow'] = value
            value = value.replace(' ', '___') if value else None
        elif isinstance(value, str):
            value = value.replace('|', '\|')
            value = value.replace('[', '\[')
            value = value.replace(']', '\]')
            value = value.replace('\n', ' ')
        if key in '_depkeys':
            value = [{dep: dep.replace(' ', '___')} for dep in action[key]]
        action[key] = value
    action.update(actionadd)
    args.doc.applyTemplate(action)
    params.result = (args.doc, args.doc)
    return params