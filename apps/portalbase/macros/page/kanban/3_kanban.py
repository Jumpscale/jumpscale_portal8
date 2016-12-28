
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
        gogs_issue['tags'] = "dashboard"
        gogs_issue['hex'] = "#36c7d0"
        gogs_issue['resourceId'] = 3
        issues.append(gogs_issue)

    issues = json.dumps(issues)
    script = j.portal.server.active.templates.render('system/kanban/script.js', issues=issues)
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
