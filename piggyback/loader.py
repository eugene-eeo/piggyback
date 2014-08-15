import os
import sys
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


class Loader(object):
    """
    Create a loader object with the given finder class and
    options.

    :param finder: The Finder class.
    :parma option: Options to provide for the finder class
        when it is requested.
    """
    def __init__(self, finder, **options):
        self.finder = finder
        self.options = options

    def get_finder(self, path):
        """
        Get a finder object for a given path. Takes the
        options that this loader object was instantiated
        with into account.

        :param path: The path.
        """
        return self.finder(path, **self.options)

    def list_modules(self, finder):
        """
        List the modules found by a given finder. Does not
        actually import anything.

        :param finder: A finder object.
        """
        iterable = finder.find_modules()
        if not finder.is_package:
            yield next(iterable)
            return

        for item in iterable:
            child = filename_to_module(item)
            yield child

    def look(self, path):
        """
        Look for the modules found in a given path. Calls
        the `list_modules` method to determine the modules.

        :param path: The path to look for.
        """
        finder = self.get_finder(path)
        iterable = self.list_modules(finder)
        for item in iterable:
            yield item

    def import_all(self, path):
        """
        Import all of the modules under the given path and
        stores them (according to their name) in a
        dictionary. All names are provided without the root of
        the path intact, i.e. if you look for modules under
        `test` you will get `mod1`, `mod2`, etc.

        :param path: The path to look under.
        """
        finder = self.get_finder(path)
        with path_context(finder.path):
            cache = {}
            for module in self.list_modules(finder):
                module_path = '%s.%s' % (finder.module_root, module)
                package = __import__(module_path, {}, {})
                cache[module] = package
            return cache

    def load(self, path, desired):
        finder = self.get_finder(path)
        with path_context(finder.path):
            for module in self.list_modules(finder):
                if module != desired:
                    continue
                module = '%s.%s' % (finder.module_root, module)
                return __import__(module, {}, {})
        raise ImportError('Module %s not found' % (desired))
