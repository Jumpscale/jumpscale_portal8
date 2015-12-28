from JumpScale.portal.docgenerator.popup import Popup

def main(j, args, params, tags, tasklet):

    params.result = page = args.page
    userguid = args.getTag('guid')
    user_model = j.data.models.getUserModel()
    group_model = j.data.models.getGroupModel()
    user = j.data.models.get(user_model,guid=userguid)

    popup = Popup(id='user_edit', header='Change User', submit_url='/restmachine/system/usermanager/editUser')

    options = list()
    popup.addText('Enter emails (comma seperated)', 'emails', value=', '.join(user.emails))
    popup.addHiddenField('domain', user.domain)
    popup.addText('Enter Password (leave empty to unchange)', 'password', type='password')
    for group in j.data.models.find(group_model,{}):
        available = group['id'] in user.groups
        options.append((group['id'], group['id'], available))

    popup.addCheckboxes('Select Groups', 'groups', options)
    popup.addHiddenField('username', user.id)
    popup.write_html(page)

    return params
