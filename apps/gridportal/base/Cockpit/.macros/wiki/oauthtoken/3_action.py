
def main(j, args, params, tags, tasklet):
    import requests
    doc = args.doc
    out = list()

    cockpit_cfg = j.portal.server.active.cfg.get('cockpit', None)
    if cockpit_cfg is None:
        out.append("cockpit configuration not present. can't reach the cockpit API")
    else:
        host = cockpit_cfg.get('host', 'localhost')
        port = cockpit_cfg.get('port', 5000)
        scheme = 'http' if host == 'localhost' else 'https'
        cockpit_url = '{scheme}://{host}:{port}/oauth/url'.format(scheme=scheme, host=host, port=port)
        resp = requests.get(cockpit_url)

        if resp.status_code != 200:
            out.append("Error during call to cockpit API")
        else:
            resp = resp.json()
            out.append('[click here to generate a new token|{url}]'.format(url=resp['url']))

    out = '\n'.join(out)
    params.result = (out, doc)

    return params
