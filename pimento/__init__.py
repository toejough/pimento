'''
Make simple python menus with pimento!
'''


# [ Imports ]
# [ -Python ]
import sys


# [ GLOBALS ]
NO_ARG=object()


# [ Private API ]
def _prompt(pre_prompt, items, post_prompt, default, indexed):
    '''
    Prompt once.
    If you want the default displayed, put a format {} into the
    post_prompt string (like 'select one [{}]: ')
    '''
    # try to sub in the default if provided
    if default is not None:
        if '{}' in pre_prompt:
            pre_prompt = pre_prompt.format(default)
        if '{}' in post_prompt:
            post_prompt = post_prompt.format(default)
    # build the item strings
    item_format = "{indent}{item}"
    if indexed:
        item_format = "{indent}[{index}] {item}"
    item_text_list = []
    indent = '  '
    for index, item in enumerate(items):
        item_text = ''
        components = {
            'indent': indent,
            'item': item
        }
        if indexed:
            components['index'] = index
        item_text = item_format.format(**components)
        item_text_list.append(item_text)
    # build full menu
    menu_parts = [pre_prompt] + item_text_list + [post_prompt]
    full_menu = '\n'.join(menu_parts)
    sys.stdout.write(full_menu)
    sys.stdout.flush()
    # Get user response
    response = raw_input()
    return response


def _check_response(response, items, default, indexed):
    '''Check the response against the items'''
    # Set selection
    selection = None
    # if indexed, check for index
    if indexed:
        if response.isdigit():
            index_response = int(response)
            if index_response < len(items):
                selection = items[index_response]
    # if not matched by an index, match by text
    if selection is None:
        # Check for text matches
        matches = [i for i in items if i.startswith(response)]
        num_matches = len(matches)
        # Empty response, no default
        if response == '' and default is None:
            print "[!] an empty response is not valid."
        elif response == '':
            selection = default
        # Bad response
        elif num_matches == 0:
            print "[!] \"{response}\" does not match any of the valid choices.".format(
                response=response
            )
        # One match
        elif num_matches == 1:
            selection = matches[0]
        # Multiple matches
        else:
            print "[!] \"{response}\" matches multiple choices:".format(
                response=response
            )
            for match in matches:
                print "[!]   {}".format(match)
            print "[!] Please specify your choice further."
    return selection


def _check_prompts(pre_prompt, post_prompt):
    '''Check that the prompts are strings'''
    if not isinstance(pre_prompt, basestring):
        raise TypeError("The pre_prompt was not a string!")
    if post_prompt is not NO_ARG and not isinstance(post_prompt, basestring):
        raise TypeError("The post_prompt was given and was not a string!")


def _check_items(items):
    '''
    Check:
     - that the list of items is iterable and finite.
     - that the list is not empty
    '''
    num_items = 0
    # Check that the list is iterable and finite
    try:
        num_items = len(items)
    except:
        raise TypeError("The item list ({}) is not a finite iterable (has no length)".format(items))
    # Check that the list has items
    if num_items == 0:
        raise ValueError("The item list is empty.")


def _check_default_index(items, default_index):
    '''Check that the default is in the list'''
    num_items = len(items)
    if default_index is not None and not isinstance(default_index, int):
        raise TypeError("The default index ({}) is not an integer".format(default_index))
    if default_index is not None and default_index >= num_items:
        raise ValueError("The default index ({}) >= length of the list ({})".format(default_index, num_items))
    if default_index is not None and default_index < 0:
        raise ValueError("The default index ({}) < 0.".format(default_index))


# [ Public API ]
def menu(pre_prompt, items, post_prompt=NO_ARG, default_index=None, indexed=False):
    '''
    Prompt with a menu.

    Arguments:
        pre_prompt -  Text to print before the option list.
        items -  The items to print as options.
        post_prompt -  Text to print after the option list.
        default_index -  The index of the item which should be default, if any.
        indexed -  Boolean.  True if the options should be indexed.

    Specifying a default index:
        The default index must index into the items.  In other words, `items[default_index]`
        must exist.  It is encouraged, but not required, that you show the user that there is
        a default, and what it is, via string interpolation in either of the prompts:
            "prompt [{}]" as the prompt string will print "prompt [default]" if "default" were
            the value of the item at the default index.

    The default post-prompt:
        The default post prompt is different depending on whether or not you provide a default_index.
        If you don't, the prompt is just "Enter an option to continue: ".
        If you do, the prompt adds the default value: "Enter an option to continue [{}]: "

    Return:
        result -  The full text of the unambiguously selected item.
    '''
    # arg checking
    _check_prompts(pre_prompt, post_prompt)
    _check_items(items)
    _check_default_index(items, default_index)
    # arg mapping
    # - Fill in post-prompt dynamically if no arg
    actual_post_prompt = post_prompt
    if post_prompt is NO_ARG:
        if default_index is None:
            actual_post_prompt = "Enter an option to continue: "
        else:
            actual_post_prompt = "Enter an option to continue [{}]: "
    # - convert items to strings
    actual_items = [str(i) for i in items]
    # - set the default argument
    default = None
    if default_index is not None:
        default = actual_items[default_index]
    # other state init
    acceptable_response_given = False
    # Prompt Loop
    # - wait until an acceptable response has been given
    while not acceptable_response_given:
        selection = None
        # Prompt and get response
        response = _prompt(pre_prompt, actual_items, actual_post_prompt, default, indexed)
        # validate response
        selection = _check_response(response, actual_items, default, indexed)
        # NOTE: acceptable response logic is purposely verbose to be clear about the semantics.
        if selection is not None:
            acceptable_response_given = True
    return selection
