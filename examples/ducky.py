import time
import usb_hid
import thumby
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

PAYLOADS = {
    "U": "/payloads/U.txt",
    "D": "/payloads/D.txt",
    "L": "/payloads/L.txt",
    "R": "/payloads/R.txt",
    "A": "/payloads/A.txt",
    "B": "/payloads/B.txt"
}

def run_ducky(filename):
    try:
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split(" ", 1)
                cmd = parts[0].upper()
                arg = parts[1] if len(parts) > 1 else ""

                if cmd == "STRING":
                    layout.write(arg)
                elif cmd == "DELAY":
                    time.sleep(int(arg) / 1000)
                elif cmd == "ENTER":
                    kbd.send(Keycode.ENTER)
                elif cmd == "GUI":
                    if arg:
                        key = getattr(Keycode, arg.upper(), None)
                        if key is not None:
                            kbd.press(Keycode.GUI, key)
                            kbd.release_all()
                    else:
                        kbd.send(Keycode.GUI)
        return True
    except OSError:
        return False

thumby.display.fill(0)
thumby.display.drawText("READY", 25, 15, 1)
thumby.display.update()

while True:
    target = None
    if thumby.buttonU.justPressed(): target = "U"
    if thumby.buttonD.justPressed(): target = "D"
    if thumby.buttonL.justPressed(): target = "L"
    if thumby.buttonR.justPressed(): target = "R"
    if thumby.buttonA.justPressed(): target = "A"
    if thumby.buttonB.justPressed(): target = "B"

    if target:
        thumby.display.fill(0)
        thumby.display.drawText(f"INJECTING {target}", 5, 15, 1)
        thumby.display.update()
        
        success = run_ducky(PAYLOADS[target])
        
        if not success:
            thumby.display.drawText("NO FILE", 5, 25, 1)
            thumby.display.update()
            time.sleep(1)
        
        thumby.display.fill(0)
        thumby.display.drawText("READY", 25, 15, 1)
        thumby.display.update()