Developing & contributing
=========================

If you are interested in getting involved in PyCoreutils, read on!


Testing
-------

The codeline is well tested. To run the tests, use::

    $ python setup.py test

Ensure that any code is compatible with Python 2.7 and 3.3+


Code style
----------

The code follows PEP8 with exemptions specified in ``setup.cfg``::

    $ flake8 pycoreutils tests


Generating the documentation
----------------------------

To generate the html documentation in docs/, install Sphinx and use:

::

   $ make html


Contributing
------------

When contributing code, you'll want to follow this checklist:

#. Fork the repository on GitHub.
#. Run the tests to confirm they all pass on your system
#. Write tests that demonstrate your bug or feature. Ensure that they fail.
#. Make your change.
#. Run the entire test suite again, confirming that all tests pass including the ones you just added.
#. Send a GitHub Pull Request

Upon merging your pull request, your name will be added to the AUTHORS.txt file!
