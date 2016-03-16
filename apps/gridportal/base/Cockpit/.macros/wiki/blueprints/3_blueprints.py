
def main(j, args, params, tags, tasklet):
    result = list()
    result.append('''{{html: <div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">}}''')

    for logpath, blueprints in j.apps.system.atyourservice.listBlueprints().items():
        repopath = j.clients.git.get(j.sal.fs.getDirName(logpath))
        repopath = '%s/%s' % (repopath.account, repopath.name)
        logs = j.sal.fs.fileGetContents(logpath)
        for blueprint in blueprints:
            bpid = blueprint.path.replace('/', '')
            bpid = bpid.rsplit('.yaml')[0]
            sectionid = 'collapse_%s' % bpid
            headingid = 'heading_%s' % bpid
            result.append("""{{html:
<div class="panel panel-default">
  <div class="panel-heading" role="tab" id="%(headingid)s">
    <h4 class="panel-title">
      <a data-toggle="collapse" data-parent="#accordion" href="#%(sectionid)s" aria-expanded="false" aria-controls="%(sectionid)s"> %(path)s</a>
    </h4>
    </div>
    <div id="%(sectionid)s" class="panel-collapse collapse" role="tabpanel" aria-labelledby="%(headingid)s">
      <div class="panel-body">
}}
h5. Blueprint
{{code:
%(content)s
}}
h5. Logs
{{code:
%(logs)s
}}
{{html:

      </div>
  </div>
</div>
}}""" % {'headingid': headingid, 'sectionid': sectionid, 'path': repopath + ':%s' % j.sal.fs.getBaseName(blueprint.path),
         'content': blueprint.content, 'logs': logs})

    result.append("""{{html:
        </div>
        }}""")
    result = '\n'.join(result)

    params.result = (result, args.doc)
    return params
