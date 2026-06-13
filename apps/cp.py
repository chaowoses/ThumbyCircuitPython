import thumby
import time

thumby.display.setFPS(60)
current_freq = 2000

def draw_interface():
    thumby.display.fill(0)
    
    thumby.display.drawText("CP TEST", 1, 1, 1)
    thumby.display.drawLine(0, 10, 72, 10, 1)

    # Up
    if thumby.buttonU.pressed(): thumby.display.drawFilledRectangle(34, 12, 4, 4, 1)
    else: thumby.display.drawRectangle(34, 12, 4, 4, 1)
    # Down
    if thumby.buttonD.pressed(): thumby.display.drawFilledRectangle(34, 22, 4, 4, 1)
    else: thumby.display.drawRectangle(34, 22, 4, 4, 1)
    # Left
    if thumby.buttonL.pressed(): thumby.display.drawFilledRectangle(29, 17, 4, 4, 1)
    else: thumby.display.drawRectangle(29, 17, 4, 4, 1)
    # Right
    if thumby.buttonR.pressed(): thumby.display.drawFilledRectangle(39, 17, 4, 4, 1)
    else: thumby.display.drawRectangle(39, 17, 4, 4, 1)

    if thumby.buttonA.pressed(): thumby.display.drawFilledRectangle(55, 17, 6, 6, 1)
    else: thumby.display.drawRectangle(55, 17, 6, 6, 1)
    thumby.display.drawText("A", 56, 25, 1)

    if thumby.buttonB.pressed(): thumby.display.drawFilledRectangle(10, 17, 6, 6, 1)
    else: thumby.display.drawRectangle(10, 17, 6, 6, 1)
    thumby.display.drawText("B", 11, 25, 1)

    thumby.display.drawText(f"Snd:{current_freq}", 1, 32, 1)

while True:
    if thumby.buttonU.pressed(): current_freq += 50
    if thumby.buttonD.pressed(): current_freq -= 50
    
    current_freq = max(100, min(5000, current_freq))

    if thumby.actionPressed():
        thumby.audio.set(current_freq)
    else:
        thumby.audio.stop()

    draw_interface()
    
    thumby.display.update()