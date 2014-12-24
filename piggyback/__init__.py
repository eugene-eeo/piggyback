"""
    piggyback
    ~~~~~~~~~

    A sane, robust, object oriented API to find and
    import modules recursively.

    :license: MIT, see LICENSE for details
    :copyright: 2014 Eugene Eeo
"""


from os.path import isdir as _isdir
from piggyback.finder import FileFinder, ModuleFinder
from piggyback.loader import Loader


def loader(path):
    """
    Returns a loader object for a given path, with
    the correct finder class (``ModuleFinder`` for
    directories and ``FileFinder`` for single file
    modules).

    :param path: The path to the module(s).
    """
    finder = ModuleFinder if _isdir(path) else FileFinder
    return Loader(finder(path))
