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
    """
    sys.path.insert(1, path)
    try:
        yield
    finally:
        sys.path.remove(path)


def filename_to_module(path):
    """
    Convert a filename to a module. Replaces the path
    separators with dots and then removes the '.py' in the
    end.
    """
    return path[:-3].replace(os.path.sep, '.')


def strip_root_module(module):
    return module.split('.', 1)[1]


def import_module(package):
    module = __import__(package, {}, {})
    for item in package.split('.')[1:]:
        module = getattr(module, item)
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
        iterable = self.finder.find_modules()
        if not self.finder.is_package:
            yield next(iterable)
            return

        for item in iterable:
            child = filename_to_module(item)
            yield child

    def import_all(self):
        """
        Import all of the modules under the given path and
        stores them (according to their name) in a
        dictionary. All names are provided without the root of
        the path intact, i.e. if you look for modules under
        `test` you will get `mod1`, `mod2`, etc.
        """
        with path_context(self.finder.path):
            cache = {}
            for module in self.search():
                module_path = '%s.%s' % (self.finder.module_root, module)
                cache[module] = import_module(module_path)
            return cache

    def load(self, desired):
        with path_context(self.finder.path):
            for module in self.search():
                if module != desired:
                    continue
                module = '%s.%s' % (self.finder.module_root, module)
                return import_module(module)
        raise ImportError('Module %s not found' % (desired))
