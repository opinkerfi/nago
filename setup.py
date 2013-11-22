# setup.py ###
from distutils.core import setup
import os

NAME = "nago"
VERSION = '0.1'
SHORT_DESC = "General purpose agent, mostly used with nagios" 
LONG_DESC = """ """


if __name__ == "__main__":
    manpath = "share/man/man1/"
    etcpath = "/etc/%s" % NAME
    etcmodpath = "/etc/%s/modules" % NAME
    initpath = "/etc/init.d/"
    logpath = "/var/log/%s/" % NAME
    varpath = "/var/lib/%s/" % NAME
    rotpath = "/etc/logrotate.d"
    datarootdir = "/usr/share/%s" % NAME
    setup(
        name='%s' % NAME,
        version=VERSION,
        author='Pall Sigurdsson',
        description=SHORT_DESC,
        long_description=LONG_DESC,
        author_email='palli@opensource.is',
        url='http://github.com/opinkerfi/nago',
        license='GPL',
        scripts=['scripts/nago'],
        packages=['nago','nago.extensions','nago.core','nago.settings','nago.protocols','nago.protocols.httpserver'],
    )
