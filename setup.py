# setup.py ###
#from distutils.core import setup
from setuptools import find_packages, setup
import os


from nago import get_version

NAME = "nago"
VERSION = get_version()
SHORT_DESC = "General purpose agent, mostly used with nagios"
LONG_DESC = """ """

datafiles = []

datadirs = ['nago/protocols/httpserver/templates/', 'etc/nago']

for i in datadirs:
    for cur_dir, dirlist, filelist in os.walk(i):
        datafiles.append(("/" + cur_dir, filelist))



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
        packages=find_packages(),
        include_package_data=True,
        package_data={'nago/protocols/httpserver': ['nago/protocols/httpserver/templates/']},
        #data_files=datafiles,
    )
