# this must be in the beginning so things are patched before ever imported by other libraries
from gevent import monkey
monkey.patch_all()
monkey.patch_socket()
monkey.patch_ssl()
monkey.patch_thread()
monkey.patch_time()

import os
import subprocess
from JumpScale import j
import JumpScale.portal
import sys

if __name__ == '__main__':
    hrd = j.data.hrd.get('%s/config.hrd' % j.sal.fs.getcwd())
    j.application.instanceconfig = hrd

    j.application.start("portal")

    server = j.core.portal.getServer()
    server.start()

    j.application.stop()
