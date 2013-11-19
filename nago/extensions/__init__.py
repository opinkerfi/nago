from nago.core import nago_access, get_peer
import inspect

__localaccess__ = object()


class NagoError(Exception):
    pass


class ExtensionError(NagoError):
    pass



__loaded_extensions = {}


@nago_access
def test():
    print __file__, __name__


def get_extensions():
    return __loaded_extensions.keys()


def get_methods(extension_name):
    """ List all remotely accessable methods of a specified extension """
    extension = get_extension(extension_name)
    methods = []
    for name, i in inspect.getmembers(extension):
        if hasattr(i, 'nago_access'):
            methods.append(name)
    return methods

def get_method(extension_name, method_name):
    """ Return a specific python method """
    extension = get_extension(extension_name)
    method = extension.__getattribute__(method_name)
    return method

def get_extension(extension_name):
    return __loaded_extensions[extension_name]


def load(extension_name):
    extension = __import__(extension_name, globals(), locals(), [''])
    __loaded_extensions[extension_name] = extension


def call_method(token, extension_name, method_name, *args, **kwargs):
    """

    """
    method = get_method(extension_name, method_name)
    if not hasattr(method, 'nago_access'):
        raise NagoError("%s.%s is not remotely accessable" % (extension_name, method_name))

    # Check the security token, check if we have access to this method
    if token != __localaccess__:
        peer = get_peer(token)
        if peer.get('access') != 'master' and peer.get('access') != method.nago_access:
            raise NagoError("security token '%s' is not good enough to call %s.%s" % (token, extension_name, method_name))
    return method(*args, **kwargs)



if not __loaded_extensions:
    load('checkresults')
    load('facts')

    #call_method('checkresults', 'get_checkresults')
    #for i in get_extensions():
    #    print i, get_methods(i)

#call_method('123', 'checkresults', 'get_checkresults')