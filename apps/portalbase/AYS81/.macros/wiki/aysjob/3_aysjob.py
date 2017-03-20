

def main(j, args, params, tags, tasklet):
    try:
        job_id = args.getTag('jobid')
        run_id = args.getTag('runid')
        reponame = args.getTag('reponame')

        run = j.apps.system.atyourservice.getRun(reponame, run_id)
        job = None
        for step in run['steps']:
            if job:
                break
            for jb in step['jobs']:
                if jb['key'] == job_id:
                    job = jb
                    break


        def printLogs(_logs):
            logs = []
            for log in _logs:
                logs.append(("{epoch} - {category}: {log}".format(
                    epoch=j.data.time.epoch2HRDateTime(log.get('epoch')),
                    category=log.get('category', ''),
                    log=log.get('log', '')
                )))
            logs = '\n'.join(logs)
            return logs
        service = j.apps.system.atyourservice.getService(reponame, job['actor_name'], job['service_name'] )
        if job:
            job['printLogs'] = printLogs(job.get('logs', []))
            args.doc.applyTemplate({'job': job, 'actions': service['actions']})
        else:
            args.doc.applyTemplate({'error': 'No job found'})
    except Exception as e:
        args.doc.applyTemplate({'error': e.__str__()})

    params.result = (args.doc, args.doc)
    return params
