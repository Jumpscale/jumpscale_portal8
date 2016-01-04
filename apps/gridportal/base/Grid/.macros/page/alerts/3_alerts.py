
def main(j, args, params, tags, tasklet):
    page = args.page
    modifier = j.html.getPageModifierGridDataTables(page)
    ecofilter = args.getTag('eco')
    filters = None
    if ecofilter:
        filters = {'eco':ecofilter}

    def makeDetails(row, field):
        data = modifier.makeTime(row, field)
        return '<a href=alert?guid=%s>%s</a>' % (row['guid'], data)

    
    fieldnames = ('Last Time', 'Description', 'Raise Time','Close Time', 'State', 'Username')
    fieldids = ['lasttime', 'description', 'inittime', 'closetime', 'state', 'username']
    fieldvalues = (makeDetails, 'description', modifier.makeTime, modifier.makeTime, 'state', 'username')

    tableid = modifier.addTableForModel('system', 'alert', fieldids, fieldnames, fieldvalues, filters)

    modifier.addSearchOptions('#%s' % tableid)
    modifier.addSorting('#%s' % tableid, 0, 'desc')

    params.result = page
    return params

def match(j, args, params, tags, tasklet):
    return True
