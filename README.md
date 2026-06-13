# Thumby-CircuitPython-API

The first API port for the **Thumby** (RP2040) using **CircuitPython**.

While the original Thumby runs on MicroPython, this project provides a compatible library for CircuitPython users. This opens up the device to native HID (BadUSB) support, easier file handling, and the Adafruit library.

---

## Features

* **1:1 API Compatibility:** Designed to mirror the original Thumby MicroPython API (`thumby.display`, `thumby.button`, etc.).
* **Integrated BadUSB:** Built-in interpreter for Ducky-style scripts via the `/payloads` folder.
* **Example Launcher:** A menu system that launches your python scripts in `/examples`.

---

## Repository Structure

* **/lib** — Includes `thumby.py` and required Adafruit drivers (HID, SSD1306, Framebuf).
* **/examples** — Hardware test scripts (Includes `ducky.py`).
* **/payloads** — `.txt` files for HID/BadUSB injections.
* **code.py** — The main Menu Launcher.
* **font5x8.bin** — Essential binary font file for the OLED.
* **ThumbySchematic.pdf** — Hardware reference used for this implementation.

---

## Hardware Setup (Pinout)

| Component | Pin (GPIO) |
| :--- | :--- |
| **OLED SCK** | GP18 |
| **OLED MOSI** | GP19 |
| **OLED DC** | GP17 |
| **OLED CS** | GP16 |
| **OLED RESET** | GP20 |
| **Audio (PWM)** | GP28 |
| **Buttons (U, D, L, R)** | GP4, GP6, GP3, GP5 |
| **Buttons (A, B)** | GP24, GP27 |

---

## Installation

1.  **Flash CircuitPython:** Ensure your RP2040 is running CircuitPython 10.x.
2.  **Copy Files:** Drag and drop all folders and files from this repo to your `CIRCUITPY` drive.

---

### BadUSB / Payloads
This device acts as a keyboard. Trigger scripts in `/payloads/` from the main menu by pressing:
* **D-Pad Up/Down/Left/Right**: Executes `u.txt`, `d.txt`, `l.txt`, or `r.txt`.
* **Button A/B**: Executes `a.txt` or `b.txt`

---

## Example Payload Syntax
Create `.txt` files in `/payloads/` using standard Ducky Script:
```text
DELAY 500
GUI r
DELAY 200
STRING [https://www.youtube.com/watch?v=dQw4w9WgXcQ](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
ENTER
```

---

## Contributing

Since this is the first CircuitPython implementation for the Thumby, bug reports and pull requests are welcome! If you want to port an original Thumby game, simply change the import logic and it should work.

**Created by a high school junior in Virginia. First of its kind.**
