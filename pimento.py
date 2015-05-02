'''
Make simple python menus with pimento!
'''


# [ Imports ]
# [ -Python ]
import sys


# [ Private API ]
def _prompt(pre_prompt, items, post_prompt, default):
    '''
    Prompt once.
    If you want the default displayed, put a format {} into the
    post_prompt string (like 'select one [{}]: ')
    '''
    print pre_prompt
    for item in items:
        print "{indent}{item}".format(
            indent='  ',
            item=item
        )
    # try to sub in the default if provided
    if default is not None:
        try:
            post_prompt = post_prompt.format(default)
        except:
            pass
    sys.stdout.write(post_prompt)
    sys.stdout.flush()
    # Get user response
    response = raw_input()
    return response


def _check_response(response, items, default):
    '''Check the response against the items'''
    # Set selection
    selection = None
    # Check for matches
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


# [ Public API ]
def menu(pre_prompt, items, post_prompt, default_index=None):
    '''Prompt with a menu'''
    # Check that the default is in the list:
    default = None
    if default_index is not None and not isinstance(default_index, int):
        raise TypeError("The default index ({}) is not an integer".format(default_index))
    if default_index is not None and len(items) <= default_index:
        raise RuntimeError("The default index ({}) >= length of the list".format(default_index))
    elif default_index is not None:
        default = items[default_index]
    # State
    acceptable_response_given = False
    selection = None
    # Prompt Loop
    # - wait until an acceptable response has been given
    while not acceptable_response_given:
        # Prompt and get response
        response = _prompt(pre_prompt, items, post_prompt, default)
        # validate response
        selection = _check_response(response, items, default)
        if selection is not None:
            acceptable_response_given = True
    return selection
