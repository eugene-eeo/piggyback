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
        root = finder.root_module
        iterable = finder.find_modules()
        if not finder.is_package:
            yield next(iterable)
            return

        for item in iterable:
            child = filename_to_module(item)
            yield '%s.%s' % (root, child)

    def look(self, path, trim=False):
        """
        Look for the modules found in a given path. Calls
        the `list_modules` method to determine the modules.

        :param path: The path to look for.
        :param trim: Whether to trim the names of the
            returned modules. See documentation for the
            equivalent option in :meth:`Loader.import_all`.
        """
        finder = self.get_finder(path)
        iterable = self.list_modules(finder)
        for item in iterable:
            if not trim:
                yield item
                continue
            item = item.split('.', 1)[1]
            yield item

    def import_all(self, path, trim=False):
        """
        Import all of the modules under the given path and
        stores them (according to their name) in a
        dictionary. All names are provided with the root of
        the path intact, i.e. if you look for modules under
        `test` you will get `test.mod1`, `test.mod2`, etc.

        :param path: The path to look under.
        :param trim: Whether to trim the names of paths,
            i.e. instead of getting `test.mod1` you get
            just the submodule name, `mod1`.
        """
        finder = self.get_finder(path)
        with path_context(finder.path):
            cache = {}
            for module in self.list_modules(finder):
                package = __import__(module, {}, {})
                cache[module] = package
            if trim:
                results = {}
                for key, value in cache:
                    key = key.split('.', 1)[1]
                    results[key] = value
                return results
            return cache
