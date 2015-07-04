import sys, tty, termios

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
try:
    tty.setraw(sys.stdin.fileno())
    for i in range(4):
        ch = sys.stdin.read(1)
        print '\r', ch, ord(ch)
finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
