from JumpScale.portal.portal import exceptions

def main(j, args, params, tags, tasklet):
    params.merge(args)
    tags = args.tags.tags
    db = tags.pop('db')
    if db == 'ays':
        index = 'index:ays:'
    elif db == 'jobs':
        index = 'index:jobs:'

    for key, val in tags.items():
        hashkv = index + key.strip()
        if bytes(val, 'utf-8') not in j.core.db.hgetall(hashkv).keys():
            raise exceptions.NotFound('ERROR : incorrect url parameters Sent')

    params.result = (params.doc, params.doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
