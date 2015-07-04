import curses

def get_char(win):
    def get_check_next_byte():
        c = win.getch()
        if 128 <= c <= 191:
            return c
        else:
            raise UnicodeError

    bytes = []
    c = win.getch()
    if c <= 127:
        # 1 bytes
        bytes.append(c)
    elif 194 <= c <= 223:
        # 2 bytes
        bytes.append(c)
        bytes.append(get_check_next_byte())
    elif 224 <= c <= 239:
        # 3 bytes
        bytes.append(c)
        bytes.append(get_check_next_byte())
        bytes.append(get_check_next_byte())
    elif 240 <= c <= 244:
        # 4 bytes
        bytes.append(c)
        bytes.append(get_check_next_byte())
        bytes.append(get_check_next_byte())
        bytes.append(get_check_next_byte())
    else:
        # unknown
        if c == curses.KEY_UP:
            raise Exception("got key up")
    buf = ''.join([chr(b) for b in bytes])
    buf = buf.decode('utf-8')
    return buf

def getcodes(win):
    codes = []
    while True:
        try:
            ch = get_char(win)
        except KeyboardInterrupt:
            return codes
        codes.append(ch)

lst = curses.wrapper(getcodes)
print lst
for c in lst:
    print c.encode('utf-8'),
print
