import evdev, time

device = None
while device is None:
    try:
        device = evdev.InputDevice('/dev/input/event0')
    except:
        print('Waiting for keyboard')
        time.sleep(3)


def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())


print('Keyboard connection established')
device.grab()

hid_usage_id = {
    1:   0x29,  # KEY_ESC
    2:   0x1e,  # KEY_1
    3:   0x1f,  # KEY_2
    4:   0x20,  # KEY_3
    5:   0x21,  # KEY_4
    6:   0x22,  # KEY_5
    7:   0x23,  # KEY_6
    8:   0x24,  # KEY_7
    9:   0x25,  # KEY_8
    10:  0x26,  # KEY_9
    11:  0x27,  # KEY_0
    12:  0x2d,  # KEY_MINUS
    13:  0x2e,  # KEY_EQUAL
    14:  0x2a,  # KEY_BACKSPACE
    15:  0x2b,  # KEY_TAB
    16:  0x14,  # KEY_Q
    17:  0x1a,  # KEY_W
    18:  0x08,  # KEY_E
    19:  0x15,  # KEY_R
    20:  0x17,  # KEY_T
    21:  0x1c,  # KEY_Y
    22:  0x18,  # KEY_U
    23:  0x0c,  # KEY_I
    24:  0x12,  # KEY_O
    25:  0x13,  # KEY_P
    26:  0x2f,  # KEY_LEFTBRACE
    27:  0x30,  # KEY_RIGHTBRACE
    28:  0x28,  # KEY_ENTER
    30:  0x04,  # KEY_A
    31:  0x16,  # KEY_S
    32:  0x07,  # KEY_D
    33:  0x09,  # KEY_F
    34:  0x0a,  # KEY_G
    35:  0x0b,  # KEY_H
    36:  0x0d,  # KEY_J
    37:  0x0e,  # KEY_K
    38:  0x0f,  # KEY_L
    39:  0x33,  # KEY_SEMICOLON
    40:  0x34,  # KEY_APOSTROPHE
    41:  0x35,  # KEY_GRAVE
    43:  0x31,  # KEY_BACKSLASH
    44:  0x1d,  # KEY_Z
    45:  0x1b,  # KEY_X
    46:  0x06,  # KEY_C
    47:  0x19,  # KEY_V
    48:  0x05,  # KEY_B
    49:  0x11,  # KEY_N
    50:  0x10,  # KEY_M
    51:  0x36,  # KEY_COMMA
    52:  0x37,  # KEY_DOT
    53:  0x38,  # KEY_SLASH
    57:  0x2c,  # KEY_SPACE
    58:  0x39,  # KEY_CAPSLOCK
    59:  0x3a,  # KEY_F1
    60:  0x3b,  # KEY_F2
    61:  0x3c,  # KEY_F3
    62:  0x3d,  # KEY_F4
    63:  0x3e,  # KEY_F5
    64:  0x3f,  # KEY_F6
    65:  0x40,  # KEY_F7
    66:  0x41,  # KEY_F8
    67:  0x42,  # KEY_F9
    68:  0x43,  # KEY_F10
    87:  0x44,  # KEY_F11
    88:  0x45,  # KEY_F12
    102: 0x4a,  # KEY_HOME
    103: 0x52,  # KEY_UP
    104: 0x4b,  # KEY_PAGEUP
    105: 0x50,  # KEY_LEFT
    106: 0x4f,  # KEY_RIGHT
    107: 0x4d,  # KEY_END
    108: 0x51,  # KEY_DOWN
    109: 0x4e,  # KEY_PAGEDOWN
    110: 0x49,  # KEY_INSERT
    111: 0x4c,  # KEY_DELETE
}

shift = False
hid_key = 0

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        key_event = evdev.categorize(event)

        if key_event.scancode == 42 or key_event.scancode == 54:
            if key_event.keystate == 1:
                shift = True
            if key_event.keystate == 0:
                shift = False
            continue

        if key_event.keystate == 1:
            hid_key = hid_usage_id.get(key_event.scancode)
            if hid_key is not None:
                if shift:
                    write_report(chr(0xe0) + '\0' + chr(hid_key) + '\0' * 5)
                else:
                    write_report('\0' * 2 + chr(hid_key) + '\0' * 5)

            write_report('\0' * 8)
