import os
import sys
from types import ModuleType
from contextlib import contextmanager


@contextmanager
def path_context(path):
    """
    A context manager that allows you to enter a given path
    into sys.path and then safely guarantee that the path
    was removed from sys.path once the block exits.

    :param path: The path to insert into sys.path.
    """
    sys.path.insert(1, path)
    try:
        yield
    finally:
        sys.path.remove(path)


def to_module(path):
    """
    Convert a filename to a module. Replaces the path
    separators with dots and then removes the '.py' in the
    end.

    :param path: The path to the module.
    """
    return path[:-3].replace(os.path.sep, '.')


def import_module(root, package):
    """
    Import a module and then return the module object itself.
    Note that this function does some ``getattr`` behind the
    scenes in order to fetch the "real" module, and not the
    root module.

    :param root: The root module.
    :param package: The module to import.
    """
    module_name = '%s.%s' % (root, package)
    module = __import__(module_name, {}, {})
    for item in package.split('.'):
        module = getattr(module, item, None)
        if not isinstance(module, ModuleType):
            raise ImportError("No module named '%s'" % (item))
    return module


class Loader(object):
    """
    Create a loader object with the given finder class and
    options.

    :param finder: The Finder class.
    :parma option: Options to provide for the finder class
        when it is requested.
    """
    def __init__(self, finder):
        self.finder = finder

    def search(self):
        """
        List the modules found by a given finder. Does not
        actually import anything.
        """
        iterable = iter(self.finder.find_modules())
        for item in iterable:
            yield to_module(item)

    def import_all(self):
        """
        Import all of the modules under the given path and
        stores them (according to their name) in a
        dictionary. All names are provided without the root of
        the path intact, i.e. if you look for modules under
        `test` you will get `mod1`, `mod2`, etc.
        """
        root = self.finder.module_root
        with path_context(self.finder.path):
            cache = {}
            for module in self.search():
                cache[module] = import_module(root, module)
            return cache

    def load(self, module):
        """
        Load a desired *module* from the search path, and
        return the module object. You will raise an
        ``ImportError`` if the module is not found.

        :param desired: The desired module.
        """
        root = self.finder.module_root
        with path_context(self.finder.path):
            return import_module(root, module)
