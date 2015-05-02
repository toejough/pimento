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
        # Validate full response
        if response in items:
            selection = response
            acceptable_response_given = True
        # Validate partial response
        else:
            for item in items:
                if item.startswith(response):
                    selection = item
                    acceptable_response_given = True
    return selection
