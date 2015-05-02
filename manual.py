import pimento

menu = pimento.Menu("yes or no?", ['yes', 'no'], "Please choose: ")
result = menu.prompt()
print 'Result was {}'.format(result)
