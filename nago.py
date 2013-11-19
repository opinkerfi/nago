#!/usr/bin/env python
""" This is a CLI to nago """

import nago
import sys
import getopt
import optparse

import nago.extensions


def print_usage(exit_code=1):
    """ Print usage, and exit the program
    """
    print "Usage: nago peer [OPTIONS]"
    sys.exit(exit_code)


def parse_arguments(arglist=sys.argv[1:]):
    if not arglist:
        print_usage(exit_code=1)
    arg1 = arglist[0]
    if arg1 == 'peer':
        peer(arglist[1:])
    elif arg1 in nago.extensions.get_extensions():
        call_extension(arg1, *arglist[1:])
    else:
        raise Exception("invalid usage")


def call_extension(extension_name, *args, **kwargs):
    """ Call an extensions that has been loaded into nago.extentions

    First argument should a command inside that extension that will be run.

    If it is not provided, a list of all commands is printed instead.
    """
    extension = nago.extensions.get_extension(extension_name)
    available_commands = nago.extensions.get_methods(extension_name)

    options = optparse.OptionParser()
    options.usage = "Usage: nago %s <action> [OPTIONS]" % extension_name
    options.usage += '\nDESCRIPTION\n===========\n'
    options.usage += extension.__doc__
    options.usage += "\nACTIONS\n======="
    for action in available_commands:
        method = nago.extensions.get_method(extension_name, action)
        help_text = method.__doc__
        options.usage += "* %s():" % action
        options.usage += help_text

    if not args or args[0] == 'help':
        options.error("No subcommand provided.")

    command = args[0]
    method = nago.extensions.get_method(extension_name, command)
    if not command in available_commands:
        options.error("Extension %s does not have an action called %s" % (extension_name, command))
    print method(*args[1:])




def peer(arglist):
    """ This is the peer subcommand
    """
    options = optparse.OptionParser()
    options.add_option('--list', dest='list', help="List new peers", action="store_true", default=False)
    options.add_option('--all', dest='all', help="Apply to all peers", action='store_true', default=False)
    (opts,args) = options.parse_args(arglist)
    peers = nago.get_peers()
    if opts.list is True:
        for token_id, i in peers.items():
            if i.get('access') is None or opts.all:
                print i.get('host_name'), i.get('address'), token_id
    elif args:
        for i in args:
            if i not in peers:
                print "Peer not found: ", i
            else:
                print "# Details for ", i
                for key, value in peers[i].items():
                    print key, value


parse_arguments()