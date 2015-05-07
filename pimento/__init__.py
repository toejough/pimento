'''
Make simple python menus with pimento!
'''


# [ Imports ]
# [ -Python ]
import sys


# [ Private API ]
def _prompt(pre_prompt, items, post_prompt, default, indexed):
    '''
    Prompt once.
    If you want the default displayed, put a format {} into the
    post_prompt string (like 'select one [{}]: ')
    '''
    print pre_prompt
    item_format = "{indent}{item}"
    for index, item in enumerate(items):
        if indexed:
            item_format = "{{indent}}[{index}] {{item}}".format(
                index=index
            )
        print item_format.format(
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


# [ Public API ]
def menu(pre_prompt, items, post_prompt, default_index=None, indexed=False):
    '''Prompt with a menu'''
    # Check that the default is in the list:
    # TODO - pull this out/push it down
    default = None
    if default_index is not None and not isinstance(default_index, int):
        raise TypeError("The default index ({}) is not an integer".format(default_index))
    if default_index is not None and len(items) <= default_index:
        raise RuntimeError("The default index ({}) >= length of the list".format(default_index))
    elif default_index is not None:
        default = items[default_index]
    # TODO check default/prompt here, too (prompt should have a {} in it)
    # State
    acceptable_response_given = False
    selection = None
    # Prompt Loop
    # - wait until an acceptable response has been given
    while not acceptable_response_given:
        # Prompt and get response
        response = _prompt(pre_prompt, items, post_prompt, default, indexed)
        # validate response
        selection = _check_response(response, items, default, indexed)
        if selection is not None:
            acceptable_response_given = True
    return selection
