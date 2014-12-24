from os.path import isdir as _isdir
from piggyback.finder import FileFinder, ModuleFinder
from piggyback.loader import Loader


def loader(path):
    finder = ModuleFinder if _isdir(path) else FileFinder
    return Loader(finder(path))
