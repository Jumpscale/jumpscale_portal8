

def main(j, args, params, tags, tasklet):
    jobid = args.getTag('jobid')

    job = j.core.jobcontroller.db.job.get(jobid)

    #### TODO: MOVE INTO ACTOR
    # running_viewers = j.sal.process.getPidsByFilter('snakeviz')
    # if len(running_viewers) > 50: # To ensure we don't get overloaded
    #     # kill oldest
    #     pass

    stats = j.sal.fs.getTempFileName()

    job = job.objectGet()
    j.sal.fs.writeFile(filename=stats, contents=job.model.dbobj.profileData, append=False)
    cmd = "snakeviz -p 82 %s" % stats
    link = j.tools.cuisine.local.core.run(cmd)

    args.doc.applyTemplate({'link': link})
    params.result = (args.doc, args.doc)

    return params
