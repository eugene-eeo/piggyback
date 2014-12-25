import sys
from contextlib import contextmanager


@contextmanager
def path_context(path):
    sys.path.insert(1, path)
    try:
        yield
    finally:
        del sys.path[1]


def import_module(path):
    mod = __import__(path, locals={}, globals={})
    for item in path.split('.')[1:]:
        try:
            mod = getattr(mod, item)
        except AttributeError:
            raise ImportError('No module named %s' % path)
    return mod


class Loader(object):
    def __init__(self, finder):
        self.finder = finder

    def search(self):
        return self.finder.modules

    @property
    def path(self):
        return self.finder.path

    def import_all(self):
        cache = {}
        with path_context(self.path):
            for item in self.search():
                cache[item] = import_module(item)
        return cache

    def import_module(self, name):
        with path_context(self.path):
            return import_module(name)
