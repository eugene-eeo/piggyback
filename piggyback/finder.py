import os


def traverse(path, hint_function):
    """
    Traverse the directory (depth-first) recursively, and
    yields all of the files of the directory.

    :param path: The path.
    :param hint_function: A function to determine whether
        to traverse the current directory. It is called
        with the contents of each directory.
    """
    files = os.listdir(path)
    if not hint_function(files):
        return
    for item in files:
        if item.startswith('.'):
            continue
        filepath = os.path.join(path, item)
        if os.path.isdir(filepath):
            for item in traverse(filepath, hint_function):
                yield item
            continue
        yield filepath


def strip_prefix(stream, prefix):
    """
    Strip the paths from the stream of paths of a prefix.

    :param stream: The stream of paths.
    :param prefix: The prefix common to all of the paths
        (this fact wouldn't be checked by the function).
        It needn't end with the path separator.
    """
    length = len(prefix)
    if not prefix.endswith(os.path.sep):
        length += len(os.path.sep)
    for filename in stream:
        yield filename[length:]


def filter_files(stream, prefix, suffix):
    """
    Filters the files based on whether they start with a
    prefix or end with a suffix.

    :param stream: The stream of paths.
    :param prefix: The desired prefix.
    :param suffix: The desired suffix.
    """
    for path in stream:
        if path.startswith(prefix) and path.endswith(suffix):
            yield path


_default_hint = lambda x: '__init__.py' in x
_default_ignore = lambda x: x.startswith('__')


class Finder(object):
    """
    Create a finder object for the given path.

    :param path: The path.
    :param prefix: Only load files with this prefix.
    :param suffix: Only load files with this suffix (can be
        combined with the prefix option).
    """
    def __init__(self, path, prefix='', suffix='.py'):
        self.path = os.path.dirname(path)
        self.root = os.path.abspath(path)

        self.module_root = os.path.basename(path)
        self.prefix = prefix
        self.suffix = suffix

        self.hints = [_default_hint]
        self.ignored = [_default_ignore]

    @property
    def is_package(self):
        """
        Returns a value telling if the path under the
        finder object is a package.
        """
        return os.path.isdir(self.root)

    @property
    def hint_function(self):
        """
        Returns the hint function for the finder object.
        The hint function basically checks if the path
        conforms to all of the hints in the `hints`
        attribute.
        """
        def hint(path):
            return all(f(path) for f in self.hints)
        return hint

    def find_nested_modules(self):
        """
        Look for nested modules. To be called only when
        the finder object is a package (dictated by the
        `is_package` property).
        """
        stream = traverse(self.root, hint_function=self.hint_function)
        stream = strip_prefix(stream, prefix=self.root)
        stream = filter_files(
            stream,
            self.prefix,
            self.suffix
        )
        for item in stream:
            path = os.path.basename(item)
            if any(ignore(path) for ignore in self.ignored):
                continue
            yield item

    def find_modules(self):
        """
        Search for the modules under path of the finder
        object. Returns either the root path or the found
        modules depending on whether the finder object is
        a package.
        """
        if not self.is_package:
            return [self.module_root]
        return self.find_nested_modules()
