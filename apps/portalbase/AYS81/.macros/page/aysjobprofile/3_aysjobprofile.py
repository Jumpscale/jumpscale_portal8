
def main(j, args, params, tags, tasklet):
    page = args.page

    from subprocess import PIPE, Popen

    jobid = args.getTag('jobid')

    job = j.core.jobcontroller.db.jobs.get(jobid)

    stats = j.sal.fs.getTempFileName()

    running_viewers = j.sal.process.getPidsByFilterSortable('snakeviz', 'start_time')
    if len(running_viewers) > 50: # To ensure we don't get overloaded
        # kill oldest
        procstokeep = set(running_viewers[-50:-1])
        procstoremove = set(running_viewers).symmetric_difference(procstokeep)
        for p in procstoremove:
            j.sal.process.kill(p)
    job = job.objectGet()
    j.sal.fs.writeFile(filename=stats, contents=job.model.dbobj.profileData, append=False)

    p = Popen(['timeout', '1m', 'python3', '-u', '/usr/local/bin/snakeviz', '-s', stats], stdout=PIPE)

    line = p.stdout.readline().decode()
    while 'http' not in line:
        line = p.stdout.readline()
        line = line.decode()

    page.addHTML("<iframe src=%s frameborder='0' width=100%% height=600 position=absolute></iframe>" % line)

    params.result = page

    return params
