import os


def traverse(path, hint_function):
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


def strip_path(stream, path):
    length = len(path)
    if not path.endswith(os.path.sep):
        length += len(os.path.sep)
    for filename in stream:
        yield filename[length:]


def filter_files(stream, prefix, suffix):
    for filename in stream:
        if (filename.startswith(prefix) and
            filename.endswith(suffix)):
            yield filename


class Finder(object):
    hint = staticmethod(lambda x: '__init__.py' in x)
    ignored = staticmethod(lambda x: x.startswith('__'))

    def __init__(self, path, prefix='', suffix='.py'):
        self.path = os.path.abspath(path)
        self.root_module = os.path.basename(path)
        self.prefix = prefix
        self.suffix = suffix

    @property
    def is_package(self):
        return os.path.isdir(self.path)

    def find_nested_modules(self):
        stream = traverse(self.path, hint_function=self.hint)
        stream = strip_path(stream, self.path)
        stream = filter_files(
            stream,
            self.prefix,
            self.suffix
        )
        for item in stream:
            if not self.ignored(os.path.basename(item)):
                yield item

    def find_modules(self):
        if not self.is_package:
            yield self.root_module
            return
        for item in self.find_nested_modules():
            yield item
