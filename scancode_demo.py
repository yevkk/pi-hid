import evdev, time

device = None
while device is None:
    try:
        device = evdev.InputDevice('/dev/input/event5')
    except:
        print('Waiting for keyboard')
        time.sleep(3)

print('Keyboard connection established')
device.grab()

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        key_event = evdev.categorize(event)
        if key_event.keystate == 1:
            print(key_event.scancode, hex(key_event.scancode), key_event.keycode)



