'''
Make simple python menus with pimento!
'''


def menu(pre_prompt, items, post_prompt):
    '''Prompt with a menu'''
    acceptable_response_given = False
    response = None
    while not acceptable_response_given:
        print pre_prompt
        for item in items:
            print "{indent}{item}".format(
                indent='  ',
                item=item
            )
        response = raw_input(post_prompt)
        if response in items:
            acceptable_response_given = True
    return response
