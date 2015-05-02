'''
Test suite for pimento
'''


# [ Imports ]
# [ -Third Party ]
import pexpect
# [ -Project ]
import pimento


# [ Helpers ]
# [ -Setup ]
def get_menu_process():
    p = pexpect.spawn('python test_pimento.py', timeout=1)
    p.expect_exact('yes or no?')
    p.expect_exact('  yes')
    p.expect_exact('  no')
    p.expect_exact('Please choose: ')
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


# [ Manual Interaction ]
if __name__ == '__main__':
    result = pimento.menu("yes or no?", ['yes', 'no'], "Please choose: ")
    print 'Result was {}'.format(result)
