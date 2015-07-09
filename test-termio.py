import sys, tty, termios

input_buffer = []

def get_byte():
    if input_buffer:
        b = input_buffer[0]
        del input_buffer[0]
    else:
        b = ord(sys.stdin.read(1))
    return b


def push_byte(b):
    input_buffer.append(b)


def is_unicode_first_byte(first_byte):
    is_ufb = False
    if 194 <= first_byte <= 223:
        # 2 bytes
        is_ufb = True
    elif 224 <= first_byte <= 239:
        # 3 bytes
        is_ufb = True
    elif 240 <= first_byte <= 244:
        # 4 bytes
        is_ufb = True
    return is_ufb


def get_unicode(first_byte):
    is_ufb = False
    utf8_bytes = [first_byte]
    if 194 <= first_byte <= 223:
        # 2 bytes
        utf8_bytes.append(get_byte())
    elif 224 <= first_byte <= 239:
        # 3 bytes
        utf8_bytes.append(get_byte())
        utf8_bytes.append(get_byte())
    elif 240 <= first_byte <= 244:
        # 4 bytes
        utf8_bytes.append(get_byte())
        utf8_bytes.append(get_byte())
        utf8_bytes.append(get_byte())
    byte_string = ''.join([chr(b) for b in utf8_bytes])
    string = byte_string.decode('utf-8')
    return utf8_bytes, string


def get_bytes(first_byte):
    timed_out = False
    raw_bytes = [first_byte]
    while not timed_out:
        results = select.select([sys.stdin], [], [], 0.1)
        readable = results[0]
        if len(readable) == 0:
            timed_tout = True
        else:
            raw_bytes.append(get_byte())
    return raw_bytes


def is_arrow(first_byte):
    is_a = False
    if first_byte == 27:
        # escape.  Check for bracket
        second_byte = get_byte()
        if second_byte == 91:
            # final byte
            final_byte = get_byte()
            if final_byte in [65, 66, 67, 68]:
                is_a = True
            # push both bytes back on
            push_byte(second_byte)
            push_byte(final_byte)
        else:
            # push byte back on if it didn't match
            push_byte(second_byte)
    return is_a


def get_arrow(first_byte):
    s = get_byte()
    t = get_byte()
    raw_bytes = [first_byte, s, t]
    key = None
    if t == 65:
        key = 'UP'
    elif t == 66:
        key = 'DOWN'
    elif t == 67:
        key = 'RIGHT'
    elif t == 68:
        key = 'LEFT'
    else:
        raise Exception("Not an arrow key sequence: {}".format(raw_bytes))
    return raw_bytes, key


def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    byte_list = []
    key = None
    try:
        #tty.setraw(sys.stdin.fileno())
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~termios.ECHO
        new[3] = new[3] & ~termios.ICANON
        termios.tcsetattr(fd, termios.TCSADRAIN, new)

        first_byte = get_byte()
        if is_arrow(first_byte):
            # Arrow key
            byte_list, key = get_arrow(first_byte)
        elif first_byte == 9:
            # Tab key
            byte_list = [first_byte]
            key = 'TAB'
        elif first_byte == 10:
            # Tab key
            byte_list = [first_byte]
            key = 'ENTER'
        elif first_byte == 127:
            # Backspace
            byte_list = [first_byte]
            key = 'BACK'
        elif first_byte <= 127:
            # ASCII
            byte_list = [first_byte]
            key = chr(first_byte)
        elif is_unicode_first_byte(first_byte):
            # UTF-8
            byte_list, key = get_unicode(first_byte)
        else:
            # Unknown
            byte_list = get_bytes(first_byte)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return byte_list, key


if __name__ == "__main__":
    quitting = False
    while not quitting:
        raw_bytes, key = get_key()
        if key is not None:
            if key == 'q':
                quitting = True
            #print "sequence: {}".format(raw_bytes)
            #print "key: {}".format(key)
            if key == 'BACK':
                sys.stdout.write(chr(27))
                sys.stdout.write(chr(91))
                sys.stdout.write(chr(68))
                sys.stdout.write(' ')
                sys.stdout.write(chr(27))
                sys.stdout.write(chr(91))
                sys.stdout.write(chr(68))
            else:
                sys.stdout.write(key)
        else:
            print "Unknown key: {}".format(raw_bytes)
    print "got q - quitting."

