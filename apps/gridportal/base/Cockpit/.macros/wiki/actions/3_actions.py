
def main(j, args, params, tags, tasklet):
    doc = args.doc
    out = list()

    actionrunids = [runid.decode() for runid in j.core.db.keys('actions.*') if runid != b'actions.runid']
    out.append('{{html:\n <table class="table table-striped table-bordered"><tr> <th>Action RunID</th><th>Action Key</th></tr>')
    for actionrunid in actionrunids:
        runid = actionrunid.split('actions.')[1]
        for actionkey in j.core.db.hkeys(actionrunid):
            actionkey = actionkey.decode()
            actionkeyescaped = actionkey.replace(' ', '___')
            out.append('<tr><td>%(runid)s</td> <td><a href=/cockpit/action?runid=%(runid)s&actionkey=%(actionkeyescaped)s>%(actionkey)s</a></td></tr>'
                       % ({'runid': runid, 'actionkey': actionkey, 'actionkeyescaped': actionkeyescaped}))
    out.append('</table>\n}}')
    out = '\n'.join(out)
    params.result = (out, doc)

    return params
