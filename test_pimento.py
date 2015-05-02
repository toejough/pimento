import pimento
import pexpect

def test_basic():
    menu = pimento.Menu("yes or no?", ['yes', 'no'], "Please choose: ")
    out = menu._out()
    assert out == '''yes or no?
  yes
  no
Please choose: '''
    menu._choose('y')
    assert menu._result == 'yes'
    menu._choose('ye')
    assert menu._result == 'yes'
    menu._choose('yes')
    assert menu._result == 'yes'
    menu._choose('n')
    assert menu._result == 'no'
    menu._choose('no')
    assert menu._result == 'no'
    menu._choose('foo')
    assert menu._result is pimento.INVALID

def test_basic_interactive():
    p = pexpect.spawn('python manual.py')
    p.expect_exact('yes or no?')
    p.expect_exact('  yes')
    p.expect_exact('  no')
    p.expect_exact('Please choose: ')
    p.sendline('yes')
    p.expect('Result was yes')
