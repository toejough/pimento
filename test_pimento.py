'''
Test suite for pimento
'''


# [ Imports ]
# [ -Third Party ]
import pexpect
# [ -Project ]
import pimento


# [ Tests ]
def test_menu_accepts_full_response():
    p = pexpect.spawn('python test_pimento.py')
    p.expect_exact('yes or no?')
    p.expect_exact('  yes')
    p.expect_exact('  no')
    p.expect_exact('Please choose: ')
    p.sendline('yes')
    p.expect('Result was yes')


# [ Manual Interaction ]
if __name__ == '__main__':
    result = pimento.menu("yes or no?", ['yes', 'no'], "Please choose: ")
    print 'Result was {}'.format(result)
