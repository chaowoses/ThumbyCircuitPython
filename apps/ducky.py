import os
import time
import usb_hid
import thumby
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

payloads = sorted([f for f in os.listdir("/ducky_payloads") if f.endswith(".txt")])
current_selection = 0
scroll_offset = 0
VISIBLE_ITEMS = 3

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

def show_menu():
    global scroll_offset
    thumby.display.fill(0)
    if not payloads:
        thumby.display.drawText("NO PAYLOADS", 5, 15, 1)
        thumby.display.update()
        return
    thumby.display.drawText("PAYLOADS", 1, 1, 1)
    thumby.display.drawLine(0, 10, 72, 10, 1)

    if current_selection < scroll_offset:
        scroll_offset = current_selection
    if current_selection >= scroll_offset + VISIBLE_ITEMS:
        scroll_offset = current_selection - VISIBLE_ITEMS + 1

    for i in range(scroll_offset, min(scroll_offset + VISIBLE_ITEMS, len(payloads))):
        prefix = ">" if i == current_selection else " "
        name = payloads[i][:-4]
        thumby.display.drawText(prefix + name[:9], 5, 12 + ((i - scroll_offset) * 10), 1)
    thumby.display.update()

while True:
    show_menu()
    if not payloads:
        continue

    if thumby.buttonD.justPressed():
        current_selection = (current_selection + 1) % len(payloads)
    if thumby.buttonU.justPressed():
        current_selection = (current_selection - 1) % len(payloads)

    if thumby.buttonA.justPressed():
        path = "/ducky_payloads/" + payloads[current_selection]
        thumby.display.fill(0)
        thumby.display.drawText("INJECTING...", 5, 15, 1)
        thumby.display.update()

        if not run_ducky(path):
            thumby.display.drawText("FAILED", 5, 25, 1)
            thumby.display.update()
            time.sleep(1)
