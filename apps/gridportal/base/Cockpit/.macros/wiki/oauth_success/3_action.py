
def main(j, args, params, tags, tasklet):
    import requests
    doc = args.doc
    out = list()
    TOKEN_KEY = 'cockpit.oauth.tokens'

    tag_dict = tags.getDict()
    state = tag_dict.get('state', None)
    if state:
        data = j.core.db.hget(TOKEN_KEY, state)
        if data:
            data = j.data.serializer.json.loads(data)
            out.append('Access Token generated')
            out.append('access token :\n{{code:\n%s\n}}' % data['access_token'])
            out.append('scope : \n{{code:\n%s\n}}' % data['scope'])
        else:
            out.append("Not token available")
    else:
        out.append("Great Success !")

    out = '\n'.join(out)
    params.result = (out, doc)

    return params
