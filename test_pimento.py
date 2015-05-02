import pimento
import pexpect

def test_simple_valid():
    p = pexpect.spawn('python manual.py')
    p.expect_exact('yes or no?')
    p.expect_exact('  yes')
    p.expect_exact('  no')
    p.expect_exact('Please choose: ')
    p.sendline('yes')
    p.expect('Result was yes')
