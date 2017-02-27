
def main(j, args, params, tags, tasklet):
    doc = args.doc
    tags = args.tags.tags

    issues = j.tools.issuemanager.getIssueCollectionFromDB()

    data = dict()
    for issue in issues.find():
        milestone = issue.dbobj.milestone or 'no milestone'
        data.setdefault(milestone, [])
        data[milestone].append(issue.to_dict())

    args.doc.applyTemplate({'milestones': data})

    params.result = (args.doc, args.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
