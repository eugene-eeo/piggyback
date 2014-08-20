"""
    piggyback
    ~~~~~~~~~

    Easily import modules and scripts, and stop it with the
    ugly ``execfiles`` and manual ``sys.path`` management.

    :copyright: (c) 2014 Eugene Eeo
    :license: MIT, see LICENSE for details.
"""

from piggyback.loader import Loader
from piggyback.finder import Finder

__version__ = '0.1.3'


def loader(path):
    """
    Creates a new loader object with the sane defaults of
    the default Finder object.

    :param path: The path to search.
    """
    return Loader(Finder(path))
