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

    @property
    def path(self):
        return self.finder.path

    def __iter__(self):
        return self.finder.modules

    def __getitem__(self, name):
        with path_context(self.path):
            return import_module(name)

    def import_all(self):
        return dict((k, self[k]) for k in self)
