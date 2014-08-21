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


def import_module(module):
    """
    Import a module and then return the module object
    itself. Note that this function does some ``getattr``
    behind the scenes in order to fetch the "real" module,
    and not the root module.

    :param module: The module to import.
    """
    lib = __import__(module, {}, {})
    for item in module.split('.')[1:]:
        lib = getattr(lib, item, None)
        if not isinstance(lib, ModuleType):
            raise ImportError("No module named '%s'" % (item))
    return lib


class Loader(object):
    """
    Create a loader object with the given finder class and
    options.

    :param finder: The Finder class.
    """
    def __init__(self, finder):
        self.finder = finder
        self.root = self.finder.module_root
        if not self.finder.is_package:
            self.root = None

    def search(self):
        """
        List the modules found by a given finder. Does not
        actually import anything.
        """
        root_package = self.root
        for item in self.finder.find_modules():
            item = to_module(item)
            if not root_package:
                yield item
                return
            yield '%s.%s' % (root_package, item)

    def import_all(self):
        """
        Import all of the modules under the given path and
        stores them (according to their name) in a
        dictionary. All names are provided with the root of
        the path intact, i.e. if you look for modules under
        `test` you will get `test.mod1`, `test.mod2`, etc.
        """
        cache = {}
        with path_context(self.finder.path):
            for module in self.search():
                cache[module] = import_module(module)
            return cache

    def load(self, module):
        """
        Load a desired *module* from the search path, and
        return the module object. You will raise an
        ``ImportError`` if the module is not found.

        :param module: The desired module.
        """
        with path_context(self.finder.path):
            return import_module(module)
