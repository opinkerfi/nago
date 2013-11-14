import os
import string
import ConfigParser
__author__ = 'palli'


def generate_token():
    """ Generate a new random security token.

     >>> len(generate_token()) == 50
     True

     Returns:
       string
    """
    length = 50
    stringset = string.ascii_letters + string.digits
    token = ''.join([stringset[i % len(stringset)] for i in [ord(x) for x in os.urandom(length)]])
    return token


def save_token(token, host_name=None):
    """ Saves this token in our list of known peers,
    """
    cfg_file = "/etc/nago/nago.ini"
    config = ConfigParser.ConfigParser()
    config.read(cfg_file)
    if token not in config.sections():
        config.add_section(token)

    config.set(token, "host_name", host_name)

    fd = open(cfg_file, 'w')
    config.write(fd)
    fd.close()

save_token(generate_token(), host_name="localhost")
