.. Piggyback documentation master file, created by
   sphinx-quickstart on Sat Aug 16 10:10:10 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Piggyback
=========

What's Piggyback?
-----------------

Piggyback is a tiny module which allows you to properly
import other modules easily, and in an extensible manner.
The design of Piggyback is inherently simple enough, so
anyone unfamiliar with the codebase can read and understand
the code. This project aims to be used in other codebases
where they need to import modules/plugins::

    from piggyback.finder import Finder
    from piggyback.loader import Loader

    loader = Loader(Finder('path/to/modules'))
    modules = loader.import_all()
    modules['module'].function()

Installing
----------

The package is available on `PyPI`_. To install it, use
either ``pip`` or ``easy_install``::

    $ pip install Piggyback

.. _PyPI: https://pypi.python.org/pypi/Piggyback

Usage
-----

To load modules, you first have to create a ``Loader`` and
``Finder`` object. The task of the ``Loader`` object is
simply to load the modules (import them), while the task
of the ``Finder`` object is to find the modules, and pass
them to the loader. To create a loader::

    from piggyback.finder import Finder
    from piggyback.loader import Loader

    loader = Loader(Finder('path'))

Then when you want to load modules, you can simply call
the load function. For example if you want to load the
module named examples that is a submodule of the module
that the Finder object was created with, you should do::

    loader.load('path.examples')

Alternatively you can discover all modules by calling
the ``import_all`` function::

    modules = loader.import_all()
    modules['path.examples']

Note that if you use a path to a script (file) when creating
the Finder object, Piggyback will also handle that correctly
and import the file only. Also, all files starting with
double underscores will not be imported, i.e. to prevent some
side effects when ``__main__`` is called. To find out if the
path points to a script or package, you have two options::

    is_package = loader.root is not None
    is_package = loader.finder.is_package

API
---

.. autoclass:: piggyback.loader.Loader
    :members:

.. autoclass:: piggyback.finder.Finder
    :members:


Advanced Usage
--------------

You can easily customize the finder object so that it
loads only certain types of files, for example if you
want it to load only files that start with ``test_``,
you can configure it using the prefix attribute::

    finder.prefix = 'test_'

Alternatively (and a better method) is using a function
that will check if the filename doesn't start with ``test_``,
by appending a function into the ``ignored`` attribute.
What this means is that all files that *do not* start with
``test_`` are ignored. Every function that is within the
``ignored`` list will be passed the filename of every
traversed Python module::

    finder.ignored.append(lambda x: not x.startswith('test_'))

Also, you can also configure the finder to only traverse
directories that contain certain files/do not contain
certain files with the ``hints`` attribute. How this works
is that each traversed directory will be called with each
function in the ``hints`` attribute, and it will only be
yielded/taken into account if all the ``hints`` return
``True``::

    finder.hints.append(lambda files: '.notests' not in files)
