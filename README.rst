=======
pimento
=======

simple CLI menu

* `examples`_
* `features`_
* `cli`_
* `installation`_
* `testing`_
* `API deprecation notices`_

examples
========

simple CLI menu prompting
-------------------------

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

Entering ``r`` results in ``red`` being returned from the function.

User input is matched case-sensitively from the beginning of each option.  Ambiguous, null, and invalid entries are handled, an error message displayed, and the menu reprompted automatically.

This is the simplest, default usage.  For more options, see the following example and the `features`_ list.
  
cli menu with all the features
------------------------------

* custom pre-prompt
* custom post-prompt
* indexing
* default selection
* case-insensitivity
* 'fuzzy' matching
* deduplication
* removal of empty items

.. code:: python

  from pimento import menu
  result = menu(
    ['', 'RED', 'Red', 'blue', 'green', 'grey', 'green', 'light URPLE'],
    pre_prompt='Available colors:',
    post_prompt='Please select a color [{}]',
    default_index=1,
    indexed=True,
    insensitive=True,
    fuzzy=True
  )

Prints:
::

  Available colors:
    [0] RED
    [1] blue
    [2] green
    [3] grey
    [4] light URPLE
  Please select a color [blue]: 

Entering ``urple`` will result in the function returning ``light URPLE``.

features
========

* Sane defaults (see the `simple cli menu prompting`_ example)
* `custom pre-prompt`_
* `custom post-prompt`_
* `partial matches`_
* `re-prompting`_
* `tab-completion`_
* `using a default`_
* `using indices`_
* `deduplication`_
* `removal of empty items`_
* `strips trailing whitespace`_
* `case-insensitivity`_
* `arrow keys`_
* `fuzzy matching`_

custom pre-prompt
-----------------

You may specify any pre-prompt you wish to appear before the list of options:

.. code:: python

  from pimento import menu
  result = menu(
    ['red', 'blue', 'green', 'grey'],
    pre_prompt="Which color?"
  )

Prints:
::

  Which color?
    red
    blue
    green
    grey
  Enter an option to continue: 

custom post-prompt
------------------

You may specify any post-propmt you wish to appear after the list of options:

.. code:: python

  from pimento import menu
  result = menu(
    ['red', 'blue', 'green', 'grey'],
    post_prompt="Please select one: "
  )

Prints:
::

  Options:
    red
    blue
    green
    grey
  Please select one:

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

tab-completion
--------------

Tab completion of options is supported!  At the moment, this is supported via ``readline``, so this is a \*nix-only feature.
Arrow-key navigation of history and current line is also supported via the ``readline`` library.


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

using indices
-------------

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
If you expect your list of items not to need deduplication, and you care about duplicates, you should check for them prior to calling ``menu``.

The default index, if specified, will be used to select the default from the list prior to deduplication:
::

  pimento bar foo foo -d 2
  Options:
    bar
    foo
  Please select an option [foo]: <enter>

In the above example, ``pimento`` prints 'foo' to stdout.

removal of empty items
----------------------

If you pass empty items into ``menu``, it will remove them for you.  This is to prevent the following scenario:
::

  pimento ''
  Options:
  
  Please select an option: <enter>
  [!] an empty response is not valid.
  Options:
  
  Please select an option: 

You can't specify an empty choice, and an empty choice doesn't make sense anyway, so ``pimento`` removes them for you.
If all you had was empty choices, the call will fail with a ValueError about the list being empty.
If you expect your list of items not to need removal of empty items, and you care if there are any, you should check that prior to calling ``menu``.

The default index, if specified, will be used to select the default from the list prior to removal of empty items:
::

  pimento '' bar foo -d 2
  Options:
    bar
    foo
  Please select an option [foo]: <enter>

In the above example, ``pimento`` prints 'foo' to stdout.

strips trailing whitespace
--------------------------

Trailing whitespace is stripped from each option passed in.
A whitespace item is defined for ``pimento`` as it is by python - typically space, tab, newline, carriage return.

* If stripping whitespace means that the item becomes a duplicate of another item, it will be removed according to the description in `deduplication`_.
* If it means that the item becomes empty it is removed according to the description in `removal of empty items`_.

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

fuzzy matching
--------------

``menu`` will accept a ``fuzzy`` argument, which will make the menu search for the words in the user input in the words of the item string,
rather than just matching the user input from the start of the option:

.. code:: python

    from pimento import menu
    result = menu(
      ['a blue thing', 'one green thing'],
      fuzzy=True
    )

Prints:
::

    Options:
      a blue thing
      one green thing
    Enter an option to continue: 

Entering ``thing n`` will return ``one green thing``.

This method matches ``thing`` to both options (both contain the full word ``thing``), then matches ``n`` only to ``one green thing``,
because that's the only option with an unmatched ``n`` (in both ``one`` and ``green``).

arrow keys
----------

When running in a \*nix environment, ``menu`` will use the Gnu ``readline`` library to provide support for command history and the use of arrow keys to edit entered text:
::

  Options:
    foo
  Enter an option to continue: oo
  [!] "oo" does not match any of the valid choices.
  Options:
    foo
  Enter an option to continue: <up><left><left>f<enter>
  foo

In the above example, the user hit ``<up>``, which brought back 'oo' and put the cursor at the end.  They then hit ``<left>`` twice to get the cursor back to the beginning of the word, inserted 'f' to spell the valid option 'foo', and hit enter.

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
      --fuzzy, -f           search for the individual words in the user input anywhere in the item strings.

    The default for the post prompt is "Enter an option to continue: ". If
    --default-index is specified, the default option value will be printed in the
    post prompt as well.


installation
============

Latest pushed to Pypi_ (v0.6.1_)

.. _Pypi: https://pypi.python.org/pypi/pimento
.. _v0.6.1: https://github.com/toejough/pimento/releases/tag/v0.6.1

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

API deprecation notices
=======================

Prompt ordering
---------------

Prior to version 0.4.0, the signature for ``menu`` was:

.. code:: python

    def menu(pre_prompt, items, post_prompt=DEFAULT, default_index=None, indexed=False):

In v0.4.0, the signature changed to:

.. code:: python

    def menu(items, pre_prompt=DEFAULT, post_prompt=DEFAULT, default_index=None, indexed=False):

To ease transition of any users, there is special code in place to determine which order the caller is passing in ``items`` and ``pre_prompt``.  All pre-0.4.0 code should continue to work, but passing ``pre_prompt`` as the first argument is a deprecated use and should be discontinued.  Old code should be updated.  The compatibility mode will be discontinued soon, but definitely by 1.0.0.

The API was changed to allow the simplest possible calling/use of the ``menu`` function.  The original signature was chosen because I thought that there wasn't a sensible default value, but "Options:" seems sensible enough for a generic default.

Search matching
---------------

As of version 0.6.0, the ``search`` method of matching is deprecated.  It will be removed within a few releases, but definitely by v1.0.0.

``fuzzy`` matching matches the same cases, and is more versatile.
