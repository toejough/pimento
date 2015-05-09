'''
Test suite for pimento
'''


# [ Imports ]
# [ -Third Party ]
import pexpect
import pytest
# [ -Project ]
import pimento


# [ Helpers ]
def expect_color_menu_prompt(process):
    process.expect_exact('which color?')
    process.expect_exact('  red')
    process.expect_exact('  blue')
    process.expect_exact('  green')
    process.expect_exact('  black')
    process.expect_exact('  grey')
    process.expect_exact('  white')
    process.expect_exact('Please select one: ')


def get_color_menu_process():
    p = pexpect.spawn('python test_pimento.py --colors', timeout=1)
    expect_color_menu_prompt(p)
    return p


def expect_menu_prompt(process):
    process.expect_exact('yes or no?')
    process.expect_exact('  yes')
    process.expect_exact('  no')
    process.expect_exact('Please choose: ')


def get_menu_process():
    p = pexpect.spawn('python test_pimento.py --yn', timeout=1)
    expect_menu_prompt(p)
    return p


# [ Tests ]
def test_menu_accepts_full_response():
    # yes
    p = get_menu_process()
    p.sendline('yes')
    p.expect('Result is yes')
    # no
    p = get_menu_process()
    p.sendline('no')
    p.expect('Result is no')


def test_menu_rejects_unmatching_response():
    # yes
    p = get_menu_process()
    p.sendline('maybe')
    p.expect_exact('[!] "maybe" does not match any of the valid choices.')
    expect_menu_prompt(p)
    p.sendline('yes')
    p.expect('Result is yes')
    # no
    p = get_menu_process()
    p.sendline('maybe')
    p.expect_exact('[!] "maybe" does not match any of the valid choices.')
    expect_menu_prompt(p)
    p.sendline('no')
    p.expect('Result is no')


def test_menu_rejects_no_response():
    # yes
    p = get_menu_process()
    p.sendline('')
    p.expect_exact('[!] an empty response is not valid.')
    expect_menu_prompt(p)
    p.sendline('yes')
    p.expect('Result is yes')
    # no
    p = get_menu_process()
    p.sendline('')
    p.expect_exact('[!] an empty response is not valid.')
    expect_menu_prompt(p)
    p.sendline('no')
    p.expect('Result is no')


def test_menu_accepts_partial_response():
    # yes
    p = get_menu_process()
    p.sendline('y')
    p.expect('Result is yes')
    p = get_menu_process()
    p.sendline('ye')
    p.expect('Result is yes')
    # no
    p = get_menu_process()
    p.sendline('n')
    p.expect('Result is no')


def test_menu_rejects_multiple_matches():
    # blue
    p = get_color_menu_process()
    p.sendline('b')
    p.expect_exact('[!] "b" matches multiple choices:')
    p.expect_exact('[!]   blue')
    p.expect_exact('[!]   black')
    p.expect_exact('[!] Please specify your choice further.')
    expect_color_menu_prompt(p)
    p.sendline('bl')
    p.expect_exact('[!] "bl" matches multiple choices:')
    p.expect_exact('[!]   blue')
    p.expect_exact('[!]   black')
    p.expect_exact('[!] Please specify your choice further.')
    p.sendline('blu')
    p.expect('Result is blue')
    # black
    p = get_color_menu_process()
    p.sendline('bla')
    p.expect('Result is black')


def test_menu_default():
    p = pexpect.spawn('python test_pimento.py --default', timeout=1)
    p.expect_exact('Yes/No?')
    p.expect_exact('  yes')
    p.expect_exact('  no')
    p.expect_exact('Please select one [no]: ')
    p.sendline('')
    p.expect('Result is no')


def test_menu_numbered():
    p = pexpect.spawn('python test_pimento.py --numbered', timeout=1)
    p.expect_exact('Select one of the following:')
    p.expect_exact('  [0] yes')
    p.expect_exact('  [1] no')
    p.expect_exact('  [2] maybe')
    p.expect_exact('Please select by index or value [yes]: ')
    p.sendline('1')
    p.expect('Result is no')


def test_indexed_numbers():
    p = pexpect.spawn('python test_pimento.py --indexed-numbers', timeout=1)
    p.expect_exact('Select one of the following:')
    p.expect_exact('  [0] 100')
    p.expect_exact('  [1] 200')
    p.expect_exact('  [2] 300')
    p.expect_exact('Please select by index or value: ')
    p.sendline('1')
    p.expect('Result is 200')
    p = pexpect.spawn('python test_pimento.py --indexed-numbers', timeout=1)
    p.expect_exact('Select one of the following:')
    p.expect_exact('  [0] 100')
    p.expect_exact('  [1] 200')
    p.expect_exact('  [2] 300')
    p.expect_exact('Please select by index or value: ')
    p.sendline('3')
    p.expect('Result is 300')


def test_default_not_in_range():
    with pytest.raises(ValueError):
        pimento.menu("Yes/No?", ['yes', 'no'], "Please select one [{}]: ", default_index=-1)
    with pytest.raises(ValueError):
        pimento.menu("Yes/No?", ['yes', 'no'], "Please select one [{}]: ", default_index=2)


def test_default_incorrect_type():
    with pytest.raises(TypeError):
        pimento.menu("Yes/No?", ['yes', 'no'], "Please select one [{}]: ", default_index=1.5)


def test_no_items():
    with pytest.raises(ValueError):
        pimento.menu("Yes/No?", [], "Please select one: ")


def test_bad_items_type():
    with pytest.raises(TypeError):
        pimento.menu("Yes/No?", 6, "Please select one: ")
    def generator():
        x = 0
        while True:
            yield x
            x += 1
    with pytest.raises(TypeError):
        pimento.menu("Yes/No?", generator(), "Please select one: ")


def test_iterable_items():
    p = pexpect.spawn('python test_pimento.py --tuple', timeout=1)
    p.expect_exact('Select one of the following:')
    p.expect_exact('  100')
    p.expect_exact('  200')
    p.expect_exact('  300')
    p.expect_exact('Please select: ')
    p = pexpect.spawn('python test_pimento.py --string', timeout=1)
    p.expect_exact('Select one of the following:')
    p.expect_exact('  a')
    p.expect_exact('  b')
    p.expect_exact('  c')
    p.expect_exact('Please select: ')
    p = pexpect.spawn('python test_pimento.py --dictionary', timeout=1)
    p.expect_exact('Select one of the following:')
    i = p.expect_exact(['  key1', '  key2'])
    if i == 0:
        p.expect_exact('  key2')
    else:
        p.expect_exact('  key1')
    p.expect_exact('Please select: ')
    p = pexpect.spawn('python test_pimento.py --set', timeout=1)
    p.expect_exact('Select one of the following:')
    p.expect_exact('  1')
    p.expect_exact('  2')
    p.expect_exact('Please select: ')


def test_string_prompts():
    with pytest.raises(TypeError):
        pimento.menu(123, [1, 2, 3], "Please select one: ")
    with pytest.raises(TypeError):
        pimento.menu("Yes/No?", ['y', 'n'], ['prompt'])


def test_non_string_items():
    p = pexpect.spawn('python test_pimento.py --set', timeout=1)
    p.expect_exact('Select one of the following:')
    p.expect_exact('  1')
    p.expect_exact('  2')
    p.expect_exact('Please select: ')
    p.sendline('1')
    p.expect_exact('Result is 1')


def test_default_post_prompt():
    p = pexpect.spawn('python test_pimento.py --pre-only', timeout=1)
    p.expect_exact('Select one of the following:')
    p.expect_exact('  1')
    p.expect_exact('  2')
    p.expect_exact('Enter an option to continue: ')
    p = pexpect.spawn('python test_pimento.py --pre-only-default', timeout=1)
    p.expect_exact('Select one of the following:')
    p.expect_exact('  1')
    p.expect_exact('  2')
    p.expect_exact('Enter an option to continue [1]: ')


def test_post_prompt_not_string():
    # test for https://github.com/toejough/pimento/issues/15
    try:
        pimento.menu("pre-prompt", [1,2,3], 5)
    except Exception as e:
        assert "pre_prompt" not in e.message


def test_menu_documentation():
    assert pimento.menu.__doc__ == '''
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


def test_package_documentation():
    assert pimento.__doc__ == '''
    Make simple python cli menus!
    '''


# [ Manual Interaction ]
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--yn', help='yes or no prompt',
                        action='store_true')
    group.add_argument('--colors', help='colors prompt',
                        action='store_true')
    group.add_argument('--default', help='yes or no with default',
                        action='store_true')
    group.add_argument('--numbered', help='a numbered list',
                        action='store_true')
    group.add_argument('--indexed-numbers', help='a numbered list of numbers',
                        action='store_true')
    group.add_argument('--tuple', help='use a tuple',
                        action='store_true')
    group.add_argument('--string', help='use a string',
                        action='store_true')
    group.add_argument('--dictionary', help='use a dictionary',
                        action='store_true')
    group.add_argument('--set', help='use a set',
                        action='store_true')
    group.add_argument('--pre-only', help='only a pre-prompt',
                        action='store_true')
    group.add_argument('--pre-only-default', help='only a pre-prompt with a default arg',
                        action='store_true')
    args = parser.parse_args()
    if args.yn:
        result = pimento.menu("yes or no?", ['yes', 'no'], "Please choose: ")
    elif args.colors:
        result = pimento.menu(
            "which color?",
            [
                'red', 'blue', 'green',
                'black', 'grey', 'white'
             ],
            "Please select one: "
        )
    elif args.default:
        result = pimento.menu("Yes/No?", ['yes', 'no'], "Please select one [{}]: ", default_index=1)
    elif args.numbered:
        result = pimento.menu("Select one of the following:", ['yes', 'no', 'maybe'], "Please select by index or value [{}]: ", default_index=0, indexed=True)
    elif args.indexed_numbers:
        result = pimento.menu("Select one of the following:", ['100', '200', '300'], "Please select by index or value: ", indexed=True)
    elif args.tuple:
        result = pimento.menu("Select one of the following:", ('100', '200', '300'), "Please select: ")
    elif args.string:
        result = pimento.menu("Select one of the following:", 'abc', "Please select: ")
    elif args.dictionary:
        result = pimento.menu("Select one of the following:", {'key1': 'v1', 'key2': 'v2'}, "Please select: ")
    elif args.set:
        result = pimento.menu("Select one of the following:", set([1, 2]), "Please select: ")
    elif args.pre_only:
        result = pimento.menu("Select one of the following:", [1, 2])
    elif args.pre_only_default:
        result = pimento.menu("Select one of the following:", [1, 2], default_index=0)
    print 'Result is {}'.format(result)
