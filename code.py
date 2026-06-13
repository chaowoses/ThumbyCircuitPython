import os
import thumby
import time

try:
    test_files = [f for f in os.listdir("/apps") if f.endswith(".py")]
except OSError:
    test_files = []
current_selection = 0
scroll_offset = 0
VISIBLE_ITEMS = 3

def show_menu():
    global scroll_offset
    thumby.display.fill(0)
    if not test_files:
        thumby.display.drawText("NO SCRIPTS", 5, 15, 1)
        thumby.display.drawText("/apps/", 5, 25, 1)
        thumby.display.update()
        return
    thumby.display.drawText("PROGRAMS", 1, 1, 1)
    thumby.display.drawLine(0, 10, 72, 10, 1)

    if current_selection < scroll_offset:
        scroll_offset = current_selection
    if current_selection >= scroll_offset + VISIBLE_ITEMS:
        scroll_offset = current_selection - VISIBLE_ITEMS + 1

    for i in range(scroll_offset, min(scroll_offset + VISIBLE_ITEMS, len(test_files))):
        prefix = ">" if i == current_selection else " "
        display_name = test_files[i][:-3]
        thumby.display.drawText(prefix + display_name[:9], 5, 12 + ((i - scroll_offset) * 10), 1)
    
    thumby.display.update()

while True:
    show_menu()
    if not test_files:
        continue
    
    if thumby.buttonD.justPressed():
        current_selection = (current_selection + 1) % len(test_files)
    if thumby.buttonU.justPressed():
        current_selection = (current_selection - 1) % len(test_files)
        
    if thumby.buttonA.justPressed():
        selected_script = "/apps/" + test_files[current_selection]
        thumby.display.fill(0)
        thumby.display.drawText("Running...", 10, 15, 1)
        thumby.display.update()
        
        with open(selected_script, "r") as f:
            exec(f.read())
        
        time.sleep(1)