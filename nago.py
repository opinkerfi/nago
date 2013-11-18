#!/usr/bin/env python
""" This is a CLI to nago """

import nago
import sys
import getopt
import optparse


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
    elif arg1 == 'checkresults':
        checkresults(arglist[1:])


def checkresults(arglist):
    """ This is the checkresults subcommand """
    options = optparse.OptionParser()
    (opts,args) = options.parse_args(arglist)



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
