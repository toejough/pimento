'''
Make simple python menus with pimento!
'''


# [ Imports ]
# [ -Python ]
import sys


# [ Private API ]
def _prompt(pre_prompt, items, post_prompt):
    '''Prompt once'''
    print pre_prompt
    for item in items:
        print "{indent}{item}".format(
            indent='  ',
            item=item
        )
    sys.stdout.write(post_prompt)
    sys.stdout.flush()
    # Get user response
    response = raw_input()
    return response


def _check_response(response, items):
    '''Check the response against the items'''
    # Set selection
    selection = None
    # Check for matches
    matches = [i for i in items if i.startswith(response)]
    num_matches = len(matches)
    # Empty response
    if response == '':
        print "[!] an empty response is not valid."
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
def menu(pre_prompt, items, post_prompt):
    '''Prompt with a menu'''
    # State
    acceptable_response_given = False
    selection = None
    # Prompt Loop
    # - wait until an acceptable response has been given
    while not acceptable_response_given:
        # Prompt and get response
        response = _prompt(pre_prompt, items, post_prompt)
        # validate response
        selection = _check_response(response, items)
        if selection is not None:
            acceptable_response_given = True
    return selection
