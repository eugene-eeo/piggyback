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

    def look(self, path):
        finder = self.finder(path, **self.options)
        root_module = finder.root_module
        for item in finder.find_modules():
            children = path_to_module(item)
            if not finder.is_package:
                yield children
                continue
            yield '.'.join((root_module, children))

    def import_all(self, path):
        with path_context(self.get_finder(path).path):
            cache = {}
            for module in self.look(path):
                package = __import__(module, {}, {})
                cache[module] = package
            return cache
