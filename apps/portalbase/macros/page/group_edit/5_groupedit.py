from JumpScale.portal.docgenerator.popup import Popup

def main(j, args, params, tags, tasklet):

    params.result = page = args.page
    groupguid = args.getTag('guid')
    group = j.data.models.system.Group.get(guid=groupguid)

    popup = Popup(id='group_edit', header='Change Group', clearForm=False, submit_url='/restmachine/system/usermanager/editGroup')

    options = list()
    popup.addText('Enter domain', 'domain', value=group.domain)
    popup.addText('Enter description', 'description', value=group.description)
    for user in j.data.models.system.User.find({}):
        available = user['name'] in group.users
        options.append((user['name'], user['name'], available))

    popup.addCheckboxes('Select Users', 'users', options)
    popup.addHiddenField('name', group.name)
    popup.write_html(page)

    return params
