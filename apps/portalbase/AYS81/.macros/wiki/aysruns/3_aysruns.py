from collections import OrderedDict


def main(j, args, params, tags, tasklet):
    import jinja2
    params.result = page = args.page
    doc = args.doc
    arg_repo = args.getTag('repo')
    klass = 'jstimestamp'
    reponame = j.sal.fs.getBaseName(arg_repo)
    runs = j.apps.system.atyourservice.listRuns(reponame)
    if runs[reponame]:
        aysruns = list()
        for run in runs:
            run = run.objectGet()
            aysruns.append(run)
            #     runat, state = value.split('|')
            #     runid = int(key)
            #     aysrun = {'id': runid,
            #               'state': state,
            #               'sortkey': '%05d' % runid,
            #               'runat': runat}
            #     aysruns.append(aysrun)
            #
            # data[repo_path].extend(sorted(aysruns, key=lambda x: x['id']))

        args.doc.applyTemplate({'runs': aysruns, 'reponame': reponame})
    else:
        args.doc.applyTemplate({'error': 'No runs on this repo', 'reponame': reponame})

    params.result = (args.doc, args.doc)
    return params
