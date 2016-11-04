PyCoreutils: Python Coreutils
=============================

Release v\ |version|.

PyCoreutils is a pure Python implementation of standard UNIX commands
similar to what is provided by the `GNU Coreutils`_. It has no extrenal
dependencies and supports all major platforms and Python versions 2.7 and 3.3+.

.. _GNU Coreutils: https://www.gnu.org/software/coreutils/coreutils.html


Installation
------------

Pycoreutils has no external dependencies outside of the standard library:

::

   $ pip install pycoreutils


Using PyCoreutils
-----------------

The package installs a script called `pycoreutils`::

   $ pycoreutils  # List all commands
   $ pycoreutils ls


The module can also be run using directly from python::

   $ python -m pycoreutils ls


Further reading
---------------

.. toctree::
   :maxdepth: 1

   commands
   contributing

Links
-----

* `PyCoreutils on GitHub <https://github.com/davidfischer/pycoreutils>`_
