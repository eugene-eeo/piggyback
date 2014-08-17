import os


def traverse(path, hint):
    """
    Traverse the directory (depth-first) recursively, and
    yields all of the files of the directory.

    :param path: The path.
    :param hint_function: A function to determine whether
        to traverse the current directory. It is called
        with the contents of each directory.
    """
    files = os.listdir(path)
    if not hint(files):
        return
    for item in files:
        if not item.startswith('.'):
            filepath = os.path.join(path, item)
            if os.path.isdir(filepath):
                for item in traverse(filepath, hint):
                    yield item
                continue
            yield filepath


def normalize_paths(stream, prefix):
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


def filter_files(stream, prefix, suffix, ignore):
    """
    Filters the files based on whether they start with a
    prefix or end with a suffix.

    :param stream: The stream of paths.
    :param prefix: The desired prefix.
    :param suffix: The desired suffix.
    :param ignore: An ignore function- files will only
        be yielded if the function doesn't return True.
    """
    for path in stream:
        base = os.path.basename(path)
        if base.startswith(prefix) and base.endswith(suffix):
            if not ignore(base):
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
        self.is_package = os.path.isdir(self.root)
        self.prefix = prefix
        self.suffix = suffix

        self.hints = [_default_hint]
        self.ignored = [_default_ignore]

    @property
    def ignore_function(self):
        """
        Returns an ignore function for the finder object.
        The ignore function checks if any of the functions
        in the ``ignored`` attribute return True for a
        given object.
        """
        def ignore(path):
            return any(f(path) for f in self.ignored)
        return ignore

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
        stream = traverse(self.root, hint=self.hint_function)
        stream = normalize_paths(stream, prefix=self.root)
        return filter_files(
            stream,
            prefix=self.prefix,
            suffix=self.suffix,
            ignore=self.ignore_function
        )

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
