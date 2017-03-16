from collections import OrderedDict

def main(j, args, params, tags, tasklet):
    query_params = args.requestContext.params
    reponame = query_params.get('reponame', None)
    out = ""
    out = "h3. Result of simulation for repository %s \n" % reponame
    try:
        run = j.apps.system.atyourservice.simulate(reponame)
        step_data = ""
        for idx, step in enumerate(run['steps']):
            jobs = ""
            for job in step['jobs']:
                jobs += """
    - {actor_name}\t {service_name} \t{action_name} \t({state})
                """.format(actor_name=job['actor_name'], service_name=job['service_name'], action_name=job['action_name'], state=job['state'])

            step_data += """
Step {number}: ({state}):
{jobs}
            """.format(number=idx, jobs=jobs, state=step['state'])
        out += "{{code: \n" + step_data + "}}"
    except Exception as e:
        out.append(str(e))

    params.result = out, args.doc
    return params
