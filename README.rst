=======
pimento
=======

simple CLI menu

features
========

a simple cli menu
-----------------

There is a single required argument:

* items - a finite iterable (list, tuple, etc) of items which the user will be prompted to choose from

.. code:: python

  from pimento import menu
  result = menu(['red', 'blue', 'green', 'grey'])

Prints:
::

  Options:
    red
    blue
    green
    grey
  Enter an option to continue: 

You may also enter your own pre-prompt:

.. code:: python

  from pimento import menu
  result = menu(
    ['red', 'blue', 'green', 'grey'],
    "Which color?"  # <--- custom pre_prompt arg
  )

Prints:
::

  Which color?
    red
    blue
    green
    grey
  Enter an option to continue: 

You may also enter your own post-prompt:

.. code:: python

  from pimento import menu
  result = menu(
    ['red', 'blue', 'green', 'grey'],
    "which color?",
    "Please select one: "  # <--- custom post_prompt arg
  )

Prints:
::

  which color?
    red
    blue
    green
    grey

partial matches
---------------

The user can select either a full option or a partial match.  All of the following will result in the user selecting ``blue``:

* ``b``
* ``bl``
* ``blu``
* ``blue``

re-prompting
------------

When an invalid option is entered, an actionable error message is printed, and the menu is re-prompted.

when no choice is entered:
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  which color?
    red
    blue
    green
    grey
  Please select one: 
  [!] an empty response is not valid.

when an invalid choice is entered:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  which color?
    red
    blue
    green
    grey
  Please select one: brown
  [!] "brown" does not match any of the valid choices.

when an ambiguous choice is entered:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If ``gre`` was entered...
::

  which color?
    red
    blue
    green
    grey
  Please select one: gre
  [!] "gre" matches multiple choices:
  [!]   green
  [!]   grey
  [!] Please specify your choice further.

using a default
---------------

``menu`` will accept a default_index keyword argument.  ``items[default_index]`` must be valid.  An invalid index will result in an exception being raised at call time.

.. code:: python

  from pimento import menu
  result = menu(
    ['red', 'blue', 'green'],
    "which color?",
    "Please select one [{}]: ",
    default_index=0
  )

Prints:
::

  which color?
    red
    blue
    green
  Please select one [red]: 

When a default_index is provided, it is valid to enter no value.  In this case, the default value (``red``, in this example) is returned.

When a default_index is provided, if ``{}`` is present in the post-prompt, it will be replaced with the value of ``items[default_index]``.  It is recommended, but not required, that if you set a default_index, you should display the default value to the users via this substitution mechanism.

## using indices
``menu`` will accept an ``indexed`` argument.  When set to ``True``, indices will be printed with each option, and it will be valid to enter an index to choose an option.

.. code:: python

  from pimento import menu
  result = menu(
    ['red', 'blue', 'green'],
    "which color?",
    "Please select one [{}]: ",
    default_index=0,
    indexed=True
  )

Prints:
::

  which color?
    [0] red
    [1] blue
    [2] green
  Please select one [red]: 

Choosing any of the following will return ``red``:

* \<enter\> (to select the default)
* ``r``
* ``re``
* ``red``
* 0 (index)

When using indices, the selection is matched first by index, then by item.  Given the following menu...
::

  which number?
    [0] 100
    [1] 200
    [2] 300
  Please select one:

...the selection/result pairs are:

* 0 -> 100 (selection treated as index)
* 1 -> 200 (selection treated as index)
* 2 -> 300 (selection treated as index)
* 3 -> 300 (selection matched no index, matched against items)
* 10 -> 100 (selection matched no index, matched against items)
* 20 -> 200 (selection matched no index, matched against items)
* 30 -> 300 (selection matched no index, matched against items)

deduplication
-------------

If you pass multiple matching items into ``menu``, it will deduplicate them for you.  This is to prevent the following scenario:
::

  pimento foo foo
  Options:
    foo
    foo
  Please select an option: foo
  [!] "foo" matches multiple choices:
  [!]   foo
  [!]   foo
  [!] Please specify your choice further.

You can't specify a choice any further in this case, so ``pimento`` deduplicates the list for you.
If you expect your list of items not to need deduplication, you should check that prior to calling ``menu``.

case-insensitivity
------------------

``menu`` will accept an ``insensitive`` argument, which will make the menu match user input to the menu options in a case-insensitive manner.

.. code:: python

    from pimento import menu
    result = menu(
      ['RED', 'Blue', 'green'],
      insensitive=True
    )

Prints:
::

    Options:
      RED
      Blue
      green
    Enter an option to continue: 

Entering ``red`` will get you ``RED``, ``blue`` will get you ``Blue``, and ``GREEN`` will get you ``green``.

searching
---------

``menu`` will accept a ``search`` argument, which will make the menu search for the user input in the whole item string, rather than just at the start:

.. code:: python

    from pimento import menu
    result = menu(
      ['RED bull', 'Blue bonnet', 'green giant'],
      insensitive=True
    )

Prints:
::

    Options:
      RED bull
      Blue bonnet
      green giant
    Enter an option to continue: 

Entering ``bull`` will return ``RED bull``.


CLI
===

There is a standalone CLI tool of the same name (``pimento``), which is a wrapper for ``pimento.menu``, and can be used to create simple menus quickly on the command line:
::

    pimento --help
    usage: pimento [-h] [--pre TEXT] [--post TEXT] [--default-index INT]
                   [--indexed]
                   option [option ...]

    Present the user with a simple CLI menu, and return the option chosen. The
    menu is presented via stderr. The output is printed to stdout for piping.

    positional arguments:
      option                The option(s) to present to the user.

    optional arguments:
      -h, --help            show this help message and exit
      --pre TEXT, -p TEXT   The pre-prompt/title/introduction to the menu.
                            [Options:]
      --post TEXT, -P TEXT  The prompt presented to the user after the menu items.
      --default-index INT, -d INT
                            The index of the item to use as the default
      --indexed, -i         Print indices with the options, and allow the user to
                            use them to choose.
      --insensitive, -I     Perform insensitive matching. Also drops any items
                            that case-insensitively match prior items.
      --search, -s          search for the user input anywhere in the item
                            strings, not just at the beginning.


    The default for the post prompt is "Enter an option to continue: ". If
    --default-index is specified, the default option value will be printed in the
    post prompt as well.


installation
============

Latest pushed to Pypi_ (v0.5.2_)

.. _Pypi: https://pypi.python.org/pypi/pimento
.. _v0.5.2: https://github.com/toejough/pimento/releases/tag/v0.5.2

::

    pip install pimento

Latest
::

    pip install git+https://github.com/toejough/pimento

testing
=======

pimento has been tested on python 2.7.9 and 3.4.3 on OSX.  To test yourself:
::

    git clone https://github.com/toejough/pimento
    cd pimento
    pip install tox
    tox

API deprecation notice
======================

Prior to version v0.4.0, the signature for ``menu`` was:

.. code:: python

    def menu(pre_prompt, items, post_prompt=DEFAULT, default_index=None, indexed=False):

In v0.4.0, the signature changed to:

.. code:: python

    def menu(items, pre_prompt=DEFAULT, post_prompt=DEFAULT, default_index=None, indexed=False):

To ease transition of any users, there is special code in place to determine which order the caller is passing in ``items`` and ``pre_prompt``.  All pre-0.4.0 code should continue to work, but passing ``pre_prompt`` as the first argument is a deprecated use and should be discontinued.  Old code should be updated.  The compatibility mode will be discontinued soon, but definitely by 1.0.0.

The API was changed to allow the simplest possible calling/use of the ``menu`` function.  The original signature was chosen because I thought that there wasn't a sensible default value, but "Options:" seems sensible enough for a generic default.
