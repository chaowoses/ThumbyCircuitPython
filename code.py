import os
import thumby
import time

test_files = [f for f in os.listdir("/examples") if f.endswith(".py")]
current_selection = 0

def show_menu():
    thumby.display.fill(0)
    if not test_files:
        thumby.display.drawText("NO SCRIPTS", 5, 15, 1)
        thumby.display.drawText("/examples/", 5, 25, 1)
        thumby.display.update()
        return
    thumby.display.drawText("PROGRAMS", 1, 1, 1)
    thumby.display.drawLine(0, 10, 72, 10, 1)
    
    for i in range(len(test_files)):
        prefix = "> " if i == current_selection else "  "
        display_name = test_files[i][:-3]
        thumby.display.drawText(prefix + display_name[:10], 5, 12 + (i * 10), 1)
    
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
        selected_script = "/examples/" + test_files[current_selection]
        thumby.display.fill(0)
        thumby.display.drawText("Running...", 10, 15, 1)
        thumby.display.update()
        
        with open(selected_script, "r") as f:
            exec(f.read())
        
        time.sleep(1)