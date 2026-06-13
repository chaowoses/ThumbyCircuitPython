import thumby
import time

running = False
start_time = 0
elapsed = 0

def format_time(secs):
    m = int(secs // 60)
    s = int(secs % 60)
    return "{:02d}:{:02d}".format(m, s)

def draw():
    thumby.display.fill(0)
    thumby.display.drawText("STOPWATCH", 1, 1, 1)
    thumby.display.drawLine(0, 9, 72, 9, 1)
    thumby.display.drawText(format_time(elapsed), 14, 16, 1)
    thumby.display.drawText("A: Pause" if running else "A: Start", 5, 31, 1)
    thumby.display.update()

while True:
    if thumby.buttonB.justPressed():
        if thumby.confirm_exit():
            break

    if thumby.buttonA.justPressed():
        if running:
            running = False
            elapsed += time.monotonic() - start_time
        else:
            running = True
            start_time = time.monotonic()

    if running:
        now = time.monotonic()
        elapsed = elapsed + (now - start_time)
        start_time = now

    draw()
    time.sleep(0.05)
