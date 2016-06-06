

def main(j, args, params, tags, tasklet):
    doc = args.doc
    repo_name = args.getTag('aysrepo')
    if not repo_name:
        repo_name = 'ays_cockpit'
    out = ''
    
    services = j.apps.system.atyourservice.findServices(repo_name=repo_name, templatename='os.cockpit')
    if len(services) != 1:
        out = "Can't find os.cockpit service"
    else:
        print(services)
        service = services[0]
        tmpl = """h1. Welcom in the Cockpit of %(organization)s
h2. SSH access

h3. Over  SSH
Command to connect into the cockpit VM:
{{code:
ssh root@%(domain)s -p %(ssh_port)s
}}

Use the following ssh key to access the cockpit VM:
{{code:
%(private_key)s
}}

h3. Over http
Address :
[https://%(domain)s/%(shellinbox_url)s|https://%(domain)s/%(shellinbox_url)s]

h2. REST API
Base URL :
[https://%(domain)s/api|https://%(domain)s/api]
Documentation URL :
[https://%(domain)s/api/apidocs/index.html|https://%(domain)s/api/apidocs/index.html]"""
        domain = service.hrd.getStr('dns.domain')
        ssh_port = service.hrd.getStr('ssh.port')
        organization = service.hrd.getStr('oauth.organization')
        private_key = ''
        for prod in service.producers['sshkey']:
            if prod.instance == 'main':
                private_key = prod.hrd.getStr('key.priv')
        shellinbox_url = service.hrd.getStr('shellinabox.url')

        out = tmpl % {'organization':organization, 'domain':domain, 'ssh_port':ssh_port, 'private_key':private_key, 'shellinbox_url':shellinbox_url}

    params.result = (out, doc)
    return params
