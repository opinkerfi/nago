from nago.core import nago_access, get_node
import nago.core
import inspect
import os
""" Extensions module for Nago

All actual domain and check-specific logic of Nago should live as an extension.

Any method created here under @nago.core.nago_access decorator is automatically
made available to the message bus.

Take a look at facts.py for an example of a simple extension.
"""

__localaccess__ = object()  # If you are working locally on this machine, you can proof it with this
__loaded_extensions = {}    # Extensions are loaded here with the load() method


class NagoError(Exception):
    pass


class ExtensionError(NagoError):
    pass


@nago_access
def test():
    print __file__, __name__


def get_extension_names():
    """ Returns a list of the names of every loaded extension  """
    return get_extensions().keys()


def get_extensions():
    """ Returns all extensions in a dictionary  """
    return __loaded_extensions


def get_method_names(extension_name):
    """ List all remotely accessable methods of a specified extension """
    return sorted(get_methods(extension_name).keys())


def get_methods(extension_name):
    """ Return all methods in extension that have nago_access set """
    extension = get_extension(extension_name)
    methods = {}
    for name, i in inspect.getmembers(extension):
        if hasattr(i, 'nago_access'):
            api_name = i.nago_name
            methods[api_name] = i
    return methods


def get_method(extension_name, method_name):
    """ Return a specific python method """
    methods = get_methods(extension_name)
    return methods[method_name]


def get_extension(extension_name):
    return __loaded_extensions[extension_name]


def load(extension_name):
    try:
        extension = __import__(extension_name, globals(), locals(), [''])
        __loaded_extensions[extension_name] = extension
        if 'on_load' in dir(extension):
            extension.on_load()
        nago.core.log(level="info", message="API Extension loaded: %s" % extension_name)
    except Exception, e:
        nago.core.log("API Extension failed to load %s: %s" % (extension_name, e), level='error')


def call_method(token, extension_name, method_name, *args, **kwargs):
    """

    """
    method = get_method(extension_name, method_name)
    if not hasattr(method, 'nago_access'):
        raise NagoError("%s.%s is not remotely accessable" % (extension_name, method_name))

    # Check the security token, check if we have access to this method
    if token != __localaccess__:
        node = get_node(token)
        if node.get('access') != 'master' and node.get('access') != method.nago_access:
            result = {}
            result['status'] = 'error'
            result['message'] = "security token '%s' is authorized %s.%s" % (token, extension_name, method_name)
            return result
    return method(*args, **kwargs)


if not __loaded_extensions:
    # Load all extensions in the same directory as the extensions package
    extension_dir = os.path.dirname(__file__)
    for dirpath, dirnames, filenames in os.walk(extension_dir):
        for f in filenames:
            if f.endswith('.py') and f[0].isalpha():
                module_name = f[:-3]
                load(module_name)
