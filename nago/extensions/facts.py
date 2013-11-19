# -*- coding: utf-8 -*-
""" Nago facts extension.

This extension allows getting facts (via 'facter' command) about this host,

posting facts is also supported, which means the agent will store facts about a remote server in memory.

"""

facts = {}
from pynag.Utils import runCommand


def get_facts():
    """ Get all facts about this machine.

    Returns:
        json-compatible dict with all facts of this host
    """
    result = runCommand('facter --json', raise_error_on_fail=True)
    facts = result[1]
    return facts


def post_facts(token, new_facts):
    """ Store facts about a remote host in memory.

    Facts will be stored in nago.extensions.facts with the remote token as a key

    """
    facts[token] = new_facts


if __name__ == '__main__':
    my_facts = get_facts()
    post_facts("123", my_facts)

    print facts



