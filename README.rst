====
ilcs
====

A Python package of utilities for dealing with data referencing the Illinois Compiled Statutes (ILCS).

Installation
============

```
pip install git+https://github.com/sc3/python-ilcs.git
```

Features
========

Iterate through all the sections
--------------------------------

::
        >>> import ilcs
        >>> for section in ilcs.sections:
        ...     print(section)
        ...
        5 ILCS 20/0.01
        5 ILCS 20/1
        5 ILCS 20/1a
        5 ILCS 20/2
        5 ILCS 20/2a


Lookup an ILCS section based on its Illinois Revised Statutes citation 
--------------------------------------------------------------------------

::

        >>> import ilcs
        >>> sections = ilcs.lookup_by_ilrs(chapter="1", paragraph="100")
        >>> print(sections[0])
        5 ILCS 20/0.01


Useful references
=================

`Organization of the Illinois Compiled Statutes (ILCS) <http://www.ilga.gov/commission/lrb/lrbnew.htm>`_
