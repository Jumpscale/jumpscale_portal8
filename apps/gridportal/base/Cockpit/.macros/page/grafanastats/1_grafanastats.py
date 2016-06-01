def main(j, args, params, tags, tasklet):
    page = args.page
    grid = "<iframe id='ifr' width='100%' height='600' src='/grafana/dashboard/db/nodes-stats?var-node=All&theme=light'></iframe>"
    host = j.portal.server.active.cfg['grafana']['host']
    port = int(j.portal.server.active.cfg['grafana']['port'])
    cl = j.clients.grafana.get("http://%s:%s" % (host, port))
    if not cl.ping():
        page.addMessage('Grafana is unreachable')
        params.result = page
        return params

    page.addMessage(grid)
    params.result = page
    return params
