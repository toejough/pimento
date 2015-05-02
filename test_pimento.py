import pimento

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

