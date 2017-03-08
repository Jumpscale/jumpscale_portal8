
def main(j, args, params, tags, tasklet):
    from collections import OrderedDict
    doc = args.doc

    macrostr = args.macrostr.strip().strip('{{').strip('}}')
    tags = j.data.tags.getObject(macrostr, keepcase=True)
    tags = tags.getDict()
    tags.pop(args.macro)

    groupon = tags.pop('groupon', 'creationTime')
    ranges = tags.pop('ranges', '')
    ranges = ranges.split(',')

    data_collection = dict()

    schema = j.tools.issuemanager.getIssueSchema()
    issue_fileds = schema.schema.fields.keys()
    if groupon not in issue_fileds:
        args.doc.applyTemplate({'data_collection': "Issues cannot be grouped on \"%s\"" % groupon})
        params.result = (args.doc, args.doc)
        return params

    if groupon not in ['creationTime', 'modTime']:
        args.doc.applyTemplate({'data_collection': "Issues with time cannot be grouped on \"%s\". Can only be grouped on creationTime or modTime. Please use issue_reports macro instead" % groupon})
        params.result = (args.doc, args.doc)
        return params


    issues = j.tools.issuemanager.getIssueCollectionFromDB()
    users = j.tools.issuemanager.getUserCollectionFromDB()

    if 'assignees' in tags:
        userid = users.find(name=tags['assignees'])
        if userid:
            userid = userid[0].key
            tags['assignees'] = userid

    user_to_id = {user.key: user.dbobj.name for user in users.find()}

    filtered_issues = OrderedDict()

    ranges.insert(0, '0')
    ranges.append('-99999999999m') #TODO

    slices = ranges.copy()
    for idx, span in enumerate(slices[:-1]):
        def negate(val):
            if idx !=0 and not val.startswith('-'):
                return "-{}".format(val)
            return val
        tags[groupon] = [j.data.time.getEpochAgo(negate(ranges[idx + 1])), j.data.time.getEpochAgo(negate(span))]
        filtered_issues[span] = issues.find(**tags)

    for span, issues in filtered_issues.items():
        for issue in issues:
            data_collection.setdefault(span, {'resolved': [], 'closed': [], 'wontfix': [], 'inprogress': [], 'question':[], 'new':[]})
            issue = issue.to_dict()
            data_collection[span][issue['state']].append(issue)

    args.doc.applyTemplate({'data_collection': data_collection})

    params.result = (args.doc, args.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
