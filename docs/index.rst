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

    loader = Loader(Finder('/path/'))

Then when you want to load modules, you can simply call
the load function. For example if you want to load the
module named
