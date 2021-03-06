# this must be in the beginning so things are patched before ever imported by other libraries
from gevent import monkey
monkey.patch_all()
monkey.patch_socket()
monkey.patch_ssl()
monkey.patch_thread()
monkey.patch_time()

from JumpScale import j
import JumpScale.portal
import click

@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--instance', default='main', help='instance of portal')
def cli(ctx, instance):
    if ctx.invoked_subcommand is None:
        ctx.obj['INSTANCE'] = instance
        start()

@click.command()
@click.pass_context
@click.option('--instance', default='main', help='instance of portal')
def start(ctx, instance):
    instance = instance or ctx.obj.get('INSTANCE')
    hrd = j.data.hrd.get('%s/portals/%s/config.hrd' % (j.dirs.cfgDir, instance))
    j.application.instanceconfig = hrd

    j.application.start("portal")

    server = j.portal.server.get()
    server.start()

    j.application.stop()

if __name__ == '__main__':
    cli(obj={})
