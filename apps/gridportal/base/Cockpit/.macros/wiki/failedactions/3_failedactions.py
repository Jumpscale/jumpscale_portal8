
def main(j, args, params, tags, tasklet):
    doc = args.doc
    out = list()
    out.append('{{html:\n <table class="table table-striped table-bordered"><tr> <th>Action RunID</th><th>Action Key</th></tr>')
    for action in j.actions.gettodo():
        actionkeyescaped = action.key.replace(' ', '___')
        out.append('<tr><td>%(runid)s</td> <td><a href=/cockpit/failedaction?runid=%(runid)s&actionkey=%(actionkeyescaped)s>%(actionkey)s</a></td></tr>'
                   % ({'runid': action.runid, 'actionkey': action.key, 'actionkeyescaped': actionkeyescaped}))
    out.append('</table>\n}}')
    out = '\n'.join(out)
    params.result = (out, doc)

    return params
