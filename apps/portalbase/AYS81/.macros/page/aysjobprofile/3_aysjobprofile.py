
def main(j, args, params, tags, tasklet):
    page = args.page

    from subprocess import PIPE, Popen

    jobid = args.getTag('jobid')

    job = j.core.jobcontroller.db.job.get(jobid)

    # TODO: MOVE INTO ACTOR
    # running_viewers = j.sal.process.getPidsByFilter('snakeviz')
    # if len(running_viewers) > 50: # To ensure we don't get overloaded
    #     # kill oldest
    #     pass

    stats = j.sal.fs.getTempFileName()

    job = job.objectGet()
    j.sal.fs.writeFile(filename=stats, contents=job.model.dbobj.profileData, append=False)

    p = Popen(['python', '-u', '/usr/local/bin/snakeviz', '-s', stats], stdout=PIPE)

    line = p.stdout.readline().decode()
    while 'http' not in line:
        line = p.stdout.readline()
        line = line.decode()
        print(line)

    page.addHTML("<iframe src=%s frameborder='0' width=100%% height=600 position=absolute></iframe>" % line)

    params.result = page

    return params
