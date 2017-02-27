
def main(j, args, params, tags, tasklet):
    doc = args.doc
    tags = args.tags.tags

    issues = j.tools.issuemanager.getIssueCollectionFromDB()

    data = dict()
    for issue in issues.find():
        milestone = issue.dbobj.milestone or 'no milestone'
        data.setdefault(milestone, {'resolved': [], 'closed': [], 'wontfix': [], 'inprogress': [], 'question':[], 'new':[]})
        issue = issue.to_dict()
        data[milestone][issue['state']].append(issue)

    args.doc.applyTemplate({'milestones': data})

    params.result = (args.doc, args.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
