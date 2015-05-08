# pimento
simple CLI menu

# example
## create the menu with choices, a default, and indices
Prompt the user to choose a color.  Specify a default, and use indices.
```python
from pimento import menu
result = menu(
  "which color?",
  [
    'red', 'blue', 'green',
    'black', 'grey', 'white'
  ],
  "Please select one [{}]: ",
  default_index=0,
  indexed=True
)
```
Prints:
```bash
which color?
  [0] red
  [1] blue
  [2] green
  [3] black
  [4] grey
  [5] white
Please select one [red]: 
```
## Choose an option
To get `red`, the user can:
* just hit enter (to select the default)
* `r`
* `re`
* `red`
* 0 (index)

## Get the result
If the user enters any of the above options, `result` is `red`.

# installation
Latest pushed to [Pypi](https://pypi.python.org/pypi/pimento) ([v0.1.0](https://github.com/toejough/pimento/releases/tag/v0.1.0))
```bash
pip install pimento
```
Latest
```bash
pip install git+https://github.com/toejough/pimento
```

# testing
pimento has only been tested on python 2.7.9.
