"""
    piggyback.loader
    ~~~~~~~~~~~~~~~~

    Implements the Loader object that handles the
    importing of modules, independent of which
    Finder object is used.

    :license: MIT, see LICENSE for details
    :copyright: (c) 2014 Eugene Eeo
"""


import sys
from contextlib import contextmanager


@contextmanager
def path_context(path):
    """
    Inserts a given *path* into ``sys.path`` as
    the second entry, then pops it off when the
    block exits.

    :param path: The parent path to the module.
    """
    sys.path.insert(1, path)
    try:
        yield
    finally:
        del sys.path[1]


def import_module(path):
    """
    Import a module given a dotted *path* in the
    form of ``.name(.name)*``, and returns the
    last module (unlike ``__import__`` which just
    returns the first module).

    :param path: The dotted path to the module.
    """
    mod = __import__(path, locals={}, globals={})
    for item in path.split('.')[1:]:
        try:
            mod = getattr(mod, item)
        except AttributeError:
            raise ImportError('No module named %s' % path)
    return mod


class Loader(object):
    """
    A Loader object takes in a Finder and then
    allows the modules found by the finder to be
    imported.

    :param finder: A Finder object.
    """

    def __init__(self, finder):
        self.finder = finder

    @property
    def path(self):
        """
        Returns the path of the finder, i.e.
        where to find the modules.
        """
        return self.finder.path

    def __iter__(self):
        return self.finder.modules

    def __getitem__(self, name):
        with path_context(self.path):
            return import_module(name)

    def import_all(self):
        """
        Imports every found module and stores
        them into a module-name to module object
        dictionary, which is then returned.
        """
        return dict((k, self[k]) for k in self)
