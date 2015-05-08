# pimento
simple CLI menu

# examples
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
