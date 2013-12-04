import ConfigParser
import platform
import os
import os.path
import errno

_sentinel = object()

cfg_file = "/etc/nago/nago.ini"

defaults = {}
defaults['main'] = {}
defaults['main']['host_name'] = platform.node()
defaults['main']['server'] = 'nago'
defaults['main']['plugin_dir'] = '/usr/lib64/nagios/plugins/'

def get_option(option_name, section_name="main", default=_sentinel, cfg_file=cfg_file):
    """ Returns a specific option specific in a config file

    Arguments:
        option_name  -- Name of the option (example host_name)
        section_name -- Which section of the config (default: name)

    examples:
    >>> get_option("some option", default="default result")
    'default result'
    """
    defaults = get_defaults()

    # As a quality issue, we strictly disallow looking up an option that does not have a default
    # value specified in the code
    #if option_name not in defaults.get(section_name, {}) and default == _sentinel:
    #    raise ValueError("There is no default value for Option %s in section %s" % (option_name, section_name))

    # If default argument was provided, we set variable my_defaults to that
    # otherwise use the global nago defaults
    if default != _sentinel:
        my_defaults = {option_name: default}
    else:
        my_defaults = defaults.get('section_name', {})

    # Lets parse our configuration file and see what we get
    parser = get_parser(cfg_file)
    return parser.get(section_name, option_name, vars=my_defaults)


def get_defaults():
    """ Returns a dictionary of all default options in nago """
    return defaults


def get_parser(cfg_file=cfg_file):
    """ Returns a ConfigParser.ConfigParser() object for our cfg_file """
    config = ConfigParser.ConfigParser()
    config.read(cfg_file)
    return config


def set_option(section='main', cfg_file=cfg_file, **kwargs):
    """ Change an option in our configuration file """
    parser = get_parser(cfg_file=cfg_file)
    if section not in parser.sections():
        parser.add_section(section)

    for k, v in kwargs.items():
        parser.set(section=section, option=k, value=v)

    with open(cfg_file, 'w') as f:
        parser.write(f)
    return "Done"


def get_section(section_name, cfg_file=cfg_file):
    """ Returns a dictionary of an entire section """
    parser = get_parser(cfg_file=cfg_file)
    options = parser.options(section_name)
    result = {}
    for option in options:
        result[option] = parser.get(section=section_name, option=option)
    return result

def _mkdir_for_config(cfg_file=cfg_file):
    """ Given a path to a filename, make sure the directory exists """
    dirname, filename = os.path.split(cfg_file)
    try:
        os.makedirs(dirname)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dirname):
            pass
        else:
            raise


def generate_configfile(cfg_file,defaults=defaults):
    """ Write a new nago.ini config file from the defaults.

    Arguments:
        cfg_file  -- File that is written to like /etc/nago/nago.ini
        defaults  -- Dictionary with default values to use
    """
    # Create a directory if needed and write an empty file
    _mkdir_for_config(cfg_file=cfg_file)
    with open(cfg_file, 'w') as f:
        f.write('')
    for section in defaults.keys():
        set_option(section, cfg_file=cfg_file, **defaults[section])


def get(*args, **kwargs):
    """ Same as get_option() """
    return get_option(*args, **kwargs)