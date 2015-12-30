from JumpScale.portal.docgenerator.popup import Popup

def main(j, args, params, tags, tasklet):

    params.result = page = args.page
    groupguid = args.getTag('guid')
    group_model = j.data.models.Group
    group = j.data.models.get(group_model,guid=groupguid)

    popup = Popup(id='group_edit', header='Change Group', clearForm=False, submit_url='/restmachine/system/usermanager/editGroup')

    options = list()
    popup.addText('Enter domain', 'domain', value=group.domain)
    popup.addText('Enter description', 'description', value=group.description)
    for user in j.data.models.User.find({}):
        available = user['name'] in group.users
        options.append((user['name'], user['id'], available))

    popup.addCheckboxes('Select Users', 'users', options)
    popup.addHiddenField('name', group.name)
    popup.write_html(page)

    return params
