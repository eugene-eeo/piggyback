import os
import sys
from contextlib import contextmanager


@contextmanager
def path_context(path):
    sys.path.append(path)
    try:
        yield
    finally:
        sys.path.remove(path)


def path_to_module(path):
    return path.rstrip('.py')\
               .replace(os.path.sep, '.')


class Loader(object):
    def __init__(self, finder, **options):
        self.finder = finder
        self.options = options

    def get_finder(self, path):
        return self.finder(path, **self.options)

    def list_modules(self, finder):
        for item in finder.find_modules():
            children = path_to_module(item)
            if finder.is_package:
                children = '.'.join((finder.root_module, children))
            yield children

    def look(self, path):
        return self.list_modules(self.get_finder(path))

    def import_all(self, path):
        finder = self.get_finder(path)
        with path_context(finder.path):
            cache = {}
            for module in self.list_modules(finder):
                package = __import__(module, {}, {})
                cache[module] = package
            return cache
