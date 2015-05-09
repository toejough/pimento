# pimento
simple CLI menu

# features
## a simple cli menu
The minimum required options are:
* pre_prompt - the prompt to print before printing the options
* items - the items which the user will be prompted to choose from
```python
from pimento import menu
result = menu(
  "which color?",
  ['red', 'blue', 'green', 'grey']
)
```
Prints:
```
which color?
  red
  blue
  green
  grey
Enter an option to continue: 
```

You may also enter your own post-prompt:
```python
from pimento import menu
result = menu(
  "which color?",
  ['red', 'blue', 'green', 'grey'],
  "Please select one: "  # <--- custom post_prompt arg
)
```
Prints:
```
which color?
  red
  blue
  green
  grey
Please select one: 
```

## partial matches
The user can select either a full option or a partial match.  All of the following will result in the user selecting `blue`:
* `b`
* `bl`
* `blu`
* `blue`

## re-prompting
When an invalid option is entered, an actionable error message is printed, and the menu is re-prompted.
### when no choice is entered:
`[!] an empty response is not valid.`
### when an invalid choice is entered:
`[!] "brown" does not match any of the valid choices.`
### when an ambiguous choice is entered:
If `gre` was entered...
```
[!] "gre" matches multiple choices:
[!]   green
[!]   grey
[!] Please specify your choice further.
```

## using a default
`menu` will accept a default_index keyword argument.  `items[default_index]` must be valid.  An invalid index will result in an exception being raised at call time.
```python
from pimento import menu
result = menu(
  "which color?",
  ['red', 'blue', 'green'],
  "Please select one [{}]: ",
  default_index=0
)
```
Prints:
```
which color?
  red
  blue
  green
Please select one [red]: 
```
When a default_index is provided, it is valid to enter no value.  In this case, the default value (`red`, in this example) is returned.

When a default_index is provided, if `{}` is present in the post-prompt, it will be replaced with the value of `items[default_index]`.  It is recommended, but not required, that if you set a default_index, you should display the default value to the users via this substitution mechanism.

## using indices
`menu` will accept an `indexed` argument.  When set to `True`, indices will be printed with each option, and it will be valid to enter an index to choose an option.
```python
from pimento import menu
result = menu(
  "which color?",
  ['red', 'blue', 'green'],
  "Please select one [{}]: ",
  default_index=0,
  indexed=True
)
```
Prints:
```
which color?
  [0] red
  [1] blue
  [2] green
Please select one [red]: 
```
Choosing any of the following will return `red`:
* \<enter\> (to select the default)
* `r`
* `re`
* `red`
* 0 (index)

When using indices, the selection is matched first by index, then by item.  Given the following menu...
```
which number?
  [0] 100
  [1] 200
  [2] 300
Please select one:
```
...the selection/result pairs are:
* 0 -> 100 (selection treated as index)
* 1 -> 200 (selection treated as index)
* 2 -> 300 (selection treated as index)
* 3 -> 300 (selection matched no index, matched against items)
* 10 -> 100 (selection matched no index, matched against items)
* 20 -> 200 (selection matched no index, matched against items)
* 30 -> 300 (selection matched no index, matched against items)

# installation
Latest pushed to [Pypi](https://pypi.python.org/pypi/pimento) ([v0.2.0](https://github.com/toejough/pimento/releases/tag/v0.2.0))
```bash
pip install pimento
```
Latest
```bash
pip install git+https://github.com/toejough/pimento
```

# testing
pimento has only been tested on python 2.7.9.
