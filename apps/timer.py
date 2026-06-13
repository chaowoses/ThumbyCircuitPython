import thumby
import time

timer_target = 60
remaining = 60
running = False
start_time = 0
selected_digit = 0
digit_x = [21, 27, 39, 45]
weights = [600, 60, 10, 1]

def format_time(secs):
    m = int(secs // 60)
    s = int(secs % 60)
    return "{:02d}:{:02d}".format(m, s)

def draw():
    thumby.display.fill(0)
    thumby.display.drawText(format_time(remaining), 21, 12, 1)
    if not running:
        thumby.display.drawText("^", digit_x[selected_digit], 20, 1)
    thumby.display.update()

while True:
    if thumby.buttonB.justPressed():
        if thumby.confirm_exit():
            break

    if thumby.buttonA.justPressed():
        if running:
            running = False
            timer_target = max(1, int(remaining))
            remaining = timer_target
        else:
            if timer_target <= 0:
                timer_target = 60
                remaining = 60
            running = True
            start_time = time.monotonic()

    if not running:
        if thumby.buttonU.justPressed():
            timer_target = min(timer_target + weights[selected_digit], 5999)
            remaining = timer_target
        if thumby.buttonD.justPressed():
            timer_target = max(timer_target - weights[selected_digit], 0)
            remaining = timer_target
        if thumby.buttonL.justPressed():
            selected_digit = (selected_digit - 1) % 4
        if thumby.buttonR.justPressed():
            selected_digit = (selected_digit + 1) % 4

    if running:
        now = time.monotonic()
        remaining = timer_target - (now - start_time)
        if remaining <= 0:
            running = False
            remaining = 0
            timer_target = 0
            for _ in range(3):
                thumby.display.fill(0)
                thumby.display.drawText("00:00", 21, 12, 1)
                thumby.display.update()
                thumby.audio.play(880, 150)
                time.sleep(0.25)
            while True:
                if thumby.buttonA.justPressed() or thumby.buttonB.justPressed():
                    break
                time.sleep(0.1)
            timer_target = 60
            remaining = 60

    draw()
    time.sleep(0.05)
