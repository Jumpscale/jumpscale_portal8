from JumpScale.portal.docgenerator.popup import Popup

def main(j, args, params, tags, tasklet):

    params.result = page = args.page
    reload = 'noreload' not in args.tags.labels
    groupcl = j.data.models.getGroupModel()

    popup = Popup(id='user_create', header='Create User', submit_url='/restmachine/system/usermanager/create', reload_on_success=reload)

    options = list()
    popup.addText('Enter Username', 'username')
    popup.addText('Enter Emails (comma seperated)', 'emails')
    popup.addHiddenField('domain', '')
    popup.addText('Enter Password', 'password', type='password')
    for group in j.data.models.find(groupcl, query={}, redis=False):
        options.append((group['id'], group['id'], False))

    popup.addCheckboxes('Select Groups', 'groups', options)
    popup.write_html(page)

    return params
