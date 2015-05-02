'''
Make simple python menus with pimento!
'''


# [ Imports ]
# [ -Python ]
import sys


# [ Functions ]
def menu(pre_prompt, items, post_prompt):
    '''Prompt with a menu'''
    # State
    acceptable_response_given = False
    selection = None
    # Prompt Loop
    # - wait until an acceptable response has been given
    while not acceptable_response_given:
        # Prompt
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
        # Check for matches
        matches = [i for i in items if i.startswith(response)]
        num_matches = len(matches)
        if response == '':
            print "[!] an empty response is not valid."
        elif num_matches == 0:
            print "[!] \"{response}\" does not match any of the valid choices.".format(
                response=response
            )
        elif num_matches == 1:
            selection = matches[0]
            acceptable_response_given = True
        else:
            print "[!] \"{response}\" matches multiple choices:".format(
                response=response
            )
            for match in matches:
                print "[!]   {}".format(match)
            print "[!] Please specify your choice further."
    return selection
