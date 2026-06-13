import board
import digitalio
import busio
import pwmio
import time
import adafruit_ssd1306
import microcontroller
import json

_SPI_SCK = board.GP18
_SPI_MOSI = board.GP19
_DC = board.GP17
_CS = board.GP16
_RST = board.GP20
_AUDIO = board.GP28

class ThumbyButton:
    def __init__(self, pin):
        self.io = digitalio.DigitalInOut(pin)
        self.io.direction = digitalio.Direction.INPUT
        self.io.pull = digitalio.Pull.UP
        self._last_state = False

    def pressed(self):
        return not self.io.value

    def justPressed(self):
        curr = self.pressed()
        res = curr and not self._last_state
        self._last_state = curr
        return res

class ThumbyGraphics:
    def __init__(self, display):
        self.display = display
        self.width = 72
        self.height = 40
        self._fps = 30
        self._last_tick = time.monotonic()

    def setFPS(self, fps): 
        self._fps = fps

    def update(self):
        now = time.monotonic()
        wait = (1.0 / self._fps) - (now - self._last_tick)
        if wait > 0:
            time.sleep(wait)
        self.display.show()
        self._last_tick = time.monotonic()

    def fill(self, color): 
        self.display.fill(color)
        
    def brightness(self, b):
        self.display.contrast(b)
        
    def setPixel(self, x, y, c): 
        self.display.pixel(x, y, c)
        
    def getPixel(self, x, y): 
        return self.display.pixel(x, y)
        
    def drawText(self, s, x, y, c): 
        self.display.text(s, x, y, c)
        
    def drawLine(self, x1, y1, x2, y2, c): 
        self.display.line(x1, y1, x2, y2, c)
        
    def drawRectangle(self, x, y, w, h, c): 
        self.display.rect(x, y, w, h, c)
        
    def drawFilledRectangle(self, x, y, w, h, c): 
        self.display.fill_rect(x, y, w, h, c)
    
    def blit(self, data, x, y, w, h, key=-1, mirrorX=False, mirrorY=False):
        import adafruit_framebuf
        buf = bytearray(data)
        row_bytes = (w + 7) // 8
        if mirrorX:
            for row in range(h):
                start = row * row_bytes
                for i in range(row_bytes // 2):
                    a = start + i
                    b = start + row_bytes - 1 - i
                    buf[a], buf[b] = buf[b], buf[a]
                for i in range(start, start + row_bytes):
                    b = buf[i]
                    b = ((b & 0xF0) >> 4) | ((b & 0x0F) << 4)
                    b = ((b & 0xCC) >> 2) | ((b & 0x33) << 2)
                    b = ((b & 0xAA) >> 1) | ((b & 0x55) << 1)
                    buf[i] = b
        if mirrorY:
            for row in range(h // 2):
                a = row * row_bytes
                b = (h - 1 - row) * row_bytes
                for i in range(row_bytes):
                    buf[a + i], buf[b + i] = buf[b + i], buf[a + i]
        fbuf = adafruit_framebuf.FrameBuffer(buf, w, h, adafruit_framebuf.MHMSB)
        self.display.blit(fbuf, x, y, key)

class ThumbyAudio:
    def __init__(self, pin):
        self._pwm = pwmio.PWMOut(pin, variable_frequency=True)
        self._enabled = True

    def setEnabled(self, setting): 
        self._enabled = setting
        
    def stop(self): 
        self._pwm.duty_cycle = 0
        
    def set(self, freq):
        if self._enabled and freq > 0:
            self._pwm.frequency = int(freq)
            self._pwm.duty_cycle = 32768
            
    def play(self, freq, duration):
        if self._enabled:
            self.set(freq)
            time.sleep(duration / 1000)
            self.stop()

class ThumbySave:
    def __init__(self):
        self._name = "default"
        self._data = {}

    def setName(self, name): 
        self._name = name
        
    def setItem(self, key, val): 
        self._data[key] = val
        
    def getItem(self, key): 
        return self._data.get(key)
        
    def hasItem(self, key): 
        return key in self._data
        
    def delItem(self, key): 
        if key in self._data: 
            del self._data[key]
            
    def save(self):
        try:
            with open(f"/{self._name}.sav", "w") as f:
                json.dump(self._data, f)
        except OSError as e:
            if e.args[0] == 30:
                print("Read-only FS: Use boot.py to enable saving.")
            else:
                raise e

_spi = busio.SPI(_SPI_SCK, MOSI=_SPI_MOSI)
_display_raw = adafruit_ssd1306.SSD1306_SPI(
    72, 40, _spi, 
    digitalio.DigitalInOut(_DC), 
    digitalio.DigitalInOut(_RST), 
    digitalio.DigitalInOut(_CS)
)

display = ThumbyGraphics(_display_raw)
audio = ThumbyAudio(_AUDIO)
saveData = ThumbySave()

buttonU = ThumbyButton(board.GP4)
buttonD = ThumbyButton(board.GP6)
buttonL = ThumbyButton(board.GP3)
buttonR = ThumbyButton(board.GP5)
buttonA = ThumbyButton(board.GP27)
buttonB = ThumbyButton(board.GP24)

def inputPressed():
    return buttonU.pressed() or buttonD.pressed() or buttonL.pressed() or \
           buttonR.pressed() or buttonA.pressed() or buttonB.pressed()

def inputJustPressed():
    return buttonU.justPressed() or buttonD.justPressed() or buttonL.justPressed() or \
           buttonR.justPressed() or buttonA.justPressed() or buttonB.justPressed()

def actionPressed():
    return buttonA.pressed() or buttonB.pressed()

def actionJustPressed():
    return buttonA.justPressed() or buttonB.justPressed()

def dpadPressed():
    return buttonU.pressed() or buttonD.pressed() or buttonL.pressed() or buttonR.pressed()

def dpadJustPressed():
    return buttonU.justPressed() or buttonD.justPressed() or buttonL.justPressed() or buttonR.justPressed()

def confirm_exit():
    display.fill(0)
    display.drawText("EXIT?", 22, 8, 1)
    display.drawLine(0, 16, 72, 16, 1)
    display.drawText("A: Back", 5, 22, 1)
    display.drawText("B: Exit", 5, 32, 1)
    display.update()
    while True:
        if buttonA.justPressed():
            return False
        if buttonB.justPressed():
            return True

def update():
    display.update()

def reset():
    microcontroller.reset()