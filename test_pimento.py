'''
Test suite for pimento
'''


# [ Imports ]
# [ -Third Party ]
import pexpect
# [ -Project ]
import pimento


# [ Helpers ]
def expect_menu_prompt(process):
    process.expect_exact('yes or no?')
    process.expect_exact('  yes')
    process.expect_exact('  no')
    process.expect_exact('Please choose: ')


def get_menu_process():
    p = pexpect.spawn('python test_pimento.py', timeout=1)
    expect_menu_prompt(p)
    return p


# [ Tests ]
def test_menu_accepts_full_response():
    # yes
    p = get_menu_process()
    p.sendline('yes')
    p.expect('Result was yes')
    # no
    p = get_menu_process()
    p.sendline('no')
    p.expect('Result was no')


def test_menu_rejects_unmatching_response():
    # yes
    p = get_menu_process()
    p.sendline('maybe')
    p.expect_exact('[!] "maybe" does not match any of the valid choices.')
    expect_menu_prompt(p)
    p.sendline('yes')
    p.expect('Result was yes')
    # no
    p = get_menu_process()
    p.sendline('maybe')
    p.expect_exact('[!] "maybe" does not match any of the valid choices.')
    expect_menu_prompt(p)
    p.sendline('no')
    p.expect('Result was no')


def test_menu_rejects_no_response():
    # yes
    p = get_menu_process()
    p.sendline('')
    p.expect_exact('[!] an empty response is not valid.')
    expect_menu_prompt(p)
    p.sendline('yes')
    p.expect('Result was yes')
    # no
    p = get_menu_process()
    p.sendline('')
    p.expect_exact('[!] an empty response is not valid.')
    expect_menu_prompt(p)
    p.sendline('no')
    p.expect('Result was no')


def test_menu_accepts_partial_response():
    # yes
    p = get_menu_process()
    p.sendline('y')
    p.expect('Result was yes')
    p = get_menu_process()
    p.sendline('ye')
    p.expect('Result was yes')
    # no
    p = get_menu_process()
    p.sendline('n')
    p.expect('Result was no')


# [ Manual Interaction ]
if __name__ == '__main__':
    result = pimento.menu("yes or no?", ['yes', 'no'], "Please choose: ")
    print 'Result was {}'.format(result)
