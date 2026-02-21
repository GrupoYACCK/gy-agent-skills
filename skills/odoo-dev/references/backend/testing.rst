.. _reference/testing:

============
Testing Odoo
============

There are many ways to test an application. In Odoo, the primary approach for backend
development is Python unit tests.

- Python unit tests: useful for testing model business logic
- Tours (integration tests): simulate real user flows via browser automation (see Odoo frontend docs)

.. _testing/python:

Testing Python code
===================

Odoo provides support for testing modules using `Python's unittest library
<https://docs.python.org/3/library/unittest.html>`_.

To write tests, simply define a ``tests`` sub-package in your module, it will
be automatically inspected for test modules. Test modules should have a name
starting with ``test_`` and should be imported from ``tests/__init__.py``,
e.g.

.. code-block:: text

    your_module
    ├── ...
    ├── tests
    |   ├── __init__.py
    |   ├── test_bar.py
    |   └── test_foo.py

and ``__init__.py`` contains::

    from . import test_foo, test_bar

.. warning::

    test modules which are not imported from ``tests/__init__.py`` will not be
    run

The test runner will simply run any test case, as described in the official
`unittest documentation`_, but Odoo provides a number of utilities and helpers
related to testing Odoo content (modules, mainly):

Key test classes: ``TransactionCase`` (rollback per test), ``SingleTransactionCase`` (shared transaction),
``HttpCase`` (full HTTP with ``url_open``, ``browser_js``). Use ``@tagged()`` decorator for test selection.

By default, tests are run once right after the corresponding module has been
installed. Test cases can also be configured to run after all modules have
been installed, and not run right after the module installation::

  # coding: utf-8
  from odoo.tests import HttpCase, tagged

  # This test should only be executed after all modules have been installed.
  @tagged('-at_install', 'post_install')
  class WebsiteVisitorTests(HttpCase):
    def test_create_visitor_on_tracked_page(self):
        Page = self.env['website.page']

The most common situation is to use
:class:`~odoo.tests.TransactionCase` and test a property of a model
in each method::

    class TestModelA(TransactionCase):
        def test_some_action(self):
            record = self.env['model.a'].create({'field': 'value'})
            record.some_action()
            self.assertEqual(
                record.field,
                expected_field_value)

        # other tests...

.. note::

    Test methods must start with ``test_``

Use ``Form(record)`` to test view-level logic (onchanges, defaults). Related proxies:
``M2MProxy`` (add/remove/clear) and ``O2MProxy`` (new/edit/remove).

Running tests
-------------

Tests are automatically run when installing or updating modules if
:option:`--test-enable <odoo-bin --test-enable>` was enabled when starting the
Odoo server.

.. _unittest documentation: https://docs.python.org/3/library/unittest.html

.. _developer/reference/testing/selection:

Test selection
--------------

In Odoo, Python tests can be tagged to facilitate the test selection when
running tests.

Subclasses of :class:`odoo.tests.BaseCase` (usually through
:class:`~odoo.tests.TransactionCase` or
:class:`~odoo.tests.HttpCase`) are automatically tagged with
``standard`` and ``at_install`` by default.

Invocation
~~~~~~~~~~

:option:`--test-tags <odoo-bin --test-tags>` can be used to select/filter tests
to run on the command-line. It implies :option:`--test-enable <odoo-bin --test-enable>`,
so it's not necessary to specify :option:`--test-enable <odoo-bin --test-enable>`
when using :option:`--test-tags <odoo-bin --test-tags>`.

This option defaults to ``+standard`` meaning tests tagged ``standard``
(explicitly or implicitly) will be run by default when starting Odoo
with :option:`--test-enable <odoo-bin --test-enable>`.

When writing tests, the :func:`~odoo.tests.tagged` decorator can be
used on **test classes** to add or remove tags.

The decorator's arguments are tag names, as strings.

.. danger:: :func:`~odoo.tests.tagged` is a class decorator, it has no
            effect on functions or methods

Tags can be prefixed with the minus (``-``) sign, to *remove* them instead of
add or select them e.g. if you don't want your test to be executed by
default you can remove the ``standard`` tag:

.. code-block:: python

    from odoo.tests import TransactionCase, tagged

    @tagged('-standard', 'nice')
    class NiceTest(TransactionCase):
        ...

This test will not be selected by default, to run it the relevant tag will
have to be selected explicitly:

.. code-block:: console

    $ odoo-bin --test-tags nice

Note that only the tests tagged ``nice`` are going to be executed. To run
*both* ``nice`` and ``standard`` tests, provide multiple values to
:option:`--test-tags <odoo-bin --test-tags>`: on the command-line, values
are *additive* (you're selecting all tests with *any* of the specified tags)

.. code-block:: console

    $ odoo-bin --test-tags nice,standard

The config switch parameter also accepts the ``+`` and ``-`` prefixes. The
``+`` prefix is implied and therefore, totally optional. The ``-`` (minus)
prefix is made to deselect tests tagged with the prefixed tags, even if they
are selected by other specified tags e.g. if there are ``standard`` tests which
are also tagged as ``slow`` you can run all standard tests *except* the slow
ones:

.. code-block:: console

    $ odoo-bin --test-tags 'standard,-slow'

When you write a test that does not inherit from the
:class:`~odoo.tests.BaseCase`, this test will not have the default tags,
you have to add them explicitly to have the test included in the default test
suite.  This is a common issue when using a simple ``unittest.TestCase`` as
they're not going to get run:

.. code-block:: python

    import unittest
    from odoo.tests import tagged

    @tagged('standard', 'at_install')
    class SmallTest(unittest.TestCase):
        ...

Besides tags you can also specify specific modules, classes or functions to
test. The full syntax of the format accepted by :option:`--test-tags <odoo-bin --test-tags>`
is:

.. code-block:: text

    [-][tag][/module][:class][.method]

So if you want to test the `stock_account` module, you can use:

    .. code-block:: console

        $ odoo-bin --test-tags /stock_account

If you want to test a specific function with a unique name, it can be specified
directly:

    .. code-block:: console

        $ odoo-bin --test-tags .test_supplier_invoice_forwarded_by_internal_user_without_supplier

This is equivalent to

    .. code-block:: console

        $ odoo-bin --test-tags /account:TestAccountIncomingSupplierInvoice.test_supplier_invoice_forwarded_by_internal_user_without_supplier

if the name of the test is unambiguous. Multiple modules, classes and functions
can be specified at once separated by a `,` like with regular tags.

.. _reference/testing/tags:

Special tags
~~~~~~~~~~~~

- ``standard``: All Odoo tests that inherit from
  :class:`~odoo.tests.BaseCase` are implicitly tagged standard.
  :option:`--test-tags <odoo-bin --test-tags>` also defaults to ``standard``.

  That means untagged test will be executed by default when tests are enabled.
- ``at_install``: Means that the test will be executed right after the module
  installation and before other modules are installed. This is a default
  implicit tag.
- ``post_install``: Means that the test will be executed after all the modules
  are installed. This is what you want for HttpCase tests most of the time.

  Note that this is *not exclusive* with ``at_install``, however since you
  will generally not want both ``post_install`` is usually paired with
  ``-at_install`` when tagging a test class.

Examples
~~~~~~~~

.. important::

    Tests will be executed only in installed modules. If you're starting from
    a clean database, you'll need to install the modules with the
    :option:`-i <odoo-bin -i>` switch at least once. After that it's no longer
    needed, unless you need to upgrade the module, in which case
    :option:`-u <odoo-bin -u>` can be used. For simplicity, those switches are
    not specified in the examples below.

Run only the tests from the sale module:

.. code-block:: console

    $ odoo-bin --test-tags /sale

Run the tests from the sale module but not the ones tagged as slow:

.. code-block:: console

    $ odoo-bin --test-tags '/sale,-slow'

Run only the tests from stock or tagged as slow:

.. code-block:: console

    $ odoo-bin --test-tags '-standard, slow, /stock'

.. note:: ``-standard`` is implicit (not required), and present for clarity





Performance Testing
===================

Query counts
------------

One of the ways to test performance is to measure database queries. Manually, this can be tested with the
`--log-sql` CLI parameter. If you want to establish the maximum number of queries for an operation,
you can use the :meth:`~odoo.tests.BaseCase.assertQueryCount` method, integrated in Odoo test classes.

.. code-block:: python

    with self.assertQueryCount(11):
        do_something()

.. _qunit_config.js: https://github.com/odoo/odoo/blob/51ee0c3cb59810449a60dae0b086b49b1ed6f946/addons/web/static/tests/helpers/qunit_config.js#L49