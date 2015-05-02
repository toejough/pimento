'''
Make simple python menus with pimento!
'''


INVALID = object()
TOO_MANY = object()


class Menu(object):
    '''Main menu class'''
    def __init__(self, prompt, items, post_prompt):
        '''Init the menu'''
        self._prompt = prompt
        self.items = items
        self.post_prompt = post_prompt
        self._result = None

    def _choose(self, choice):
        '''Choose a value from the menu'''
        matches = [i for i in self.items if i.startswith(choice)]
        num_matches = len(matches)
        if num_matches == 0:
            self._result = INVALID
        elif num_matches == 1:
            self._result = matches[0]
        else:
            self._result = TOO_MANY

    def _out(self):
        '''The menu output'''
        text = self._prompt
        for i in self.items:
            text += '\n  {}'.format(i)
        text += '\n{}'.format(self.post_prompt)
        return text

    def prompt(self):
        '''Prompt the user and return the result'''
        while self._result is None:
            self._choose(raw_input(self._out()))
            if self._result is INVALID:
                self._result = None
            if self._result is TOO_MANY:
                self._result = None
        return self._result
