
def main(j, args, params, tags, tasklet):
    doc = args.doc
    tags = args.tags.tags

    issues = j.tools.issuemanager.getIssueCollectionFromDB()
    user_collection = j.tools.issuemanager.getUserCollectionFromDB()
    user_to_id = {user.key: user.dbobj.name for user in user_collection.find()}

    data = dict()
    for issue in issues.find():
        assignees = issue.dbobj.assignees or 'No assignees'
        for assignee in assignees:
            assignee = user_to_id.get(assignee, 'no assignees')
            data.setdefault(assignee, {'resolved': [], 'closed': [], 'wontfix': [], 'inprogress': [], 'question':[], 'new':[]})

            issue_dict = issue.to_dict()
            data[assignee][issue_dict['state']].append(issue_dict)

    args.doc.applyTemplate({'users': data})

    params.result = (args.doc, args.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
