
def main(j, args, params, tags, tasklet):
    page = args.page
    modifier = j.html.getPageModifierGridDataTables(page)

    fieldnames = ['Grid ID', 'Name', 'Grid Node ID', 'IP Address', 'Roles']
    filters = dict()
    for tag, val in args.tags.tags.items():
        if tag in ('gid', ) and val and not val.startswith("$$"):
            filters['gid'] = int(val)
    if args.getTag('roles'):
        filters['roles'] = args.getTag('roles')

    namelink = '[%(name)s|/grid/Grid Node?id=%(id)s&gid=%(gid)s]' # add dict here

    fieldvalues = ['gid', namelink, 'id','ipaddr', 'roles']
    fieldids = ['gid', 'name', 'id', 'ipaddr', 'roles']
    tableid = modifier.addTableForModel('system', 'node', fieldids, fieldnames, fieldvalues, filters)
    modifier.addSearchOptions('#%s' % tableid)

    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True
