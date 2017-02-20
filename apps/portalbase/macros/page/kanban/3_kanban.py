
def main(j, args, params, tags, tasklet):
    import json
    import yaml
    page = args.page

    macrostr = args.macrostr.strip()
    content = "\n".join(macrostr.split("\n")[1:-1])
    try:
        gogs_data = yaml.load(content)
    except yaml.error.YAMLError:
        page.addMessage('<h3> **ERROR : Incorrect YAML format , please adjust. </h3>')
        params.result = page
        return params

    if not isinstance(gogs_data, list):
        gogs_data = [gogs_data]

    page.addCSS("/jslib/jqwidgets/styles/jqx.base.css")
    page.addJS("/jslib/jqwidgets/jquery-1.11.1.min.js")
    page.addJS("/jslib/jqwidgets/jqxcore.js")
    page.addJS("/jslib/jqwidgets/jqxsortable.js")
    page.addJS("/jslib/jqwidgets/jqxkanban.js")
    page.addJS("/jslib/jqwidgets/jqxsplitter.js")
    page.addJS("/jslib/jqwidgets/jqxdata.js")

    # { id: "1161", state: "new", label: "Make a new Dashboard", tags: "dashboard", hex: "#36c7d0", resourceId: 3 }
    issues = list()
    for gogs_issue in gogs_data:
        if gogs_issue['state'] == 'new':
            gogs_issue['hex'] = "#009999"
        elif gogs_issue['state'] == 'work':
            gogs_issue['hex'] = "#5d88b3"
        elif gogs_issue['state'] == 'verification':
            gogs_issue['hex'] = "#f1c40f"
        else:
            gogs_issue['hex'] = "#ff5050"
        gogs_issue['resourceId'] = 3
        issues.append(gogs_issue)

    def createUserData(user):
        user = user.dictFiltered
        data = {'id': user['gogsRefs'][0]['id'],
                'name': user['name']
                }
        return data

    user_collection = j.tools.issuemanager.getUserCollectionFromDB()
    users = list(map(createUserData, user_collection.find()))
    users.append({'id': 0,
                  'name': "No name",
                  'common': 'true'})
    issues = json.dumps(issues)

    if not json.loads(issues):
        page.addMessage('No issues to show in kanban')

    script = j.portal.server.active.templates.render('system/kanban/script.js', issues=issues, users=users)
    css = j.portal.server.active.templates.render('system/kanban/style.css')
    page.addCSS(cssContent=css)

    kanban = """
    <div id="kanban1"></div>
    """

    page.addJS(jsContent=script)
    page.addHTML(kanban)

    page.addBootstrap()

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
