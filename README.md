
# Duckie with Perks

> **A tiny ride. A giant quack. Zero boring duckies.**

**Built with:**    
    <img width="41" height="41" alt="MicroPython_new_logo" src="https://github.com/user-attachments/assets/50d042ce-69cf-4c97-a30e-a11d67aa7a4e" /> <img width="41" height="41" alt="images-3" src="https://github.com/user-attachments/assets/9797e68c-7792-4ce6-8c4a-cfa02d974346" /> <img width="41" height="41" alt="github-copilot" src="https://github.com/user-attachments/assets/ebc03536-5d04-4f09-bdb1-9da2d8d5fd3a" />



Duckie with Perks is a remote-controlled duck-mobile with differential drive,
personality, and just the right amount of chaos. It is controlled by an analog
joystick and packed with custom duck-themed features:

- Differential drive with two motors
- Joystick control, including diagonal directions
- JHD1803M1 I²C LCD with duck animations and catchphrases
- Startup sound and a non-blocking “Alle meine Entchen” melody
- Button-triggered melody playback
- Smooth acceleration and a safety stop

```text
             __
         ___( o)>   QUACK MODE: ON
         \ <_. )
          `---'
```

## Hackathon: ZeFIx 2026

| | |
|---|---|
| **Date** | 13–15 November 2026 |
| **Team** | Benjamin, Grantly Marshall, Arsenji, Rik and Johannes Faizade |
| **Challenge** | Classic duckies are boring. Give them features. |
| **Our contribution** | A duck-mobile that drives, quacks on an LCD, plays “Alle meine Entchen”, and boots with style. |
| **Result** | Duckie with Perks |

<img width="3072" height="4096" alt="IMG_20261115_155215689" src="https://github.com/user-attachments/assets/a34d4aa5-d119-4b7d-b2b8-1781d18aa635" />


## Hardware

- Maker Pi RP2040
- Two DC motors with wheels
- Analog joystick module, such as the HW-505
- JHD1803M1 I²C LCD
- Push button
- 1 AAA battery slot and 2 AA battery slots

> ⚡ **Power note:** Never power the motors from the RP2040's 3.3 V output.
> The motor supply and the board must share a common ground (`GND`).

## Pinout

| Function | RP2040 pin |
|---|---:|
| Motor 1, direction A/B | GP8 / GP9 |
| Motor 2, direction A/B | GP10 / GP11 |
| Joystick X (Grove 6A) | GP26 / ADC0 |
| Joystick Y (Grove 6B) | GP27 / ADC1 |
| Push button | GP17 |
| Buzzer | GP22 |
| LCD SDA | GP4 |
| LCD SCL | GP5 |
| LCD I²C address | `0x3E` |

Connect the button between `GP17` and `GND`. The internal pull-up makes the
input `LOW` when pressed.

## Files

- `main.py` – Main program for the motors, joystick, LCD, buzzer, and button
- `i2c_lcd.py` – MicroPython driver for the LCD
- `screen_test.py` – Standalone LCD test program
- `new_test_wheels.py` – Standalone motor and joystick test program

## Setup

1. Flash MicroPython onto the Maker Pi RP2040.
2. Copy `main.py` and `i2c_lcd.py` to the board.
3. Connect the LCD, joystick, motors, and button according to the pinout.
4. Power the board with a suitable external power supply.

Use `mpremote` to copy the files:

```bash
python3 -m pip install mpremote
mpremote connect /dev/cu.usbmodemXXXX fs cp i2c_lcd.py :i2c_lcd.py
mpremote connect /dev/cu.usbmodemXXXX fs cp main.py :main.py
mpremote connect /dev/cu.usbmodemXXXX reset
```

Replace `/dev/cu.usbmodemXXXX` with the current device port. On macOS, find it
with:

```bash
ls /dev/cu.usb*
```

## Controls

Keep the joystick still when starting the program. It automatically calibrates
the center position.

| Joystick direction | Duckie response |
|---|---|
| Up | Forward |
| Down | Reverse |
| Left / right | Turn |
| Diagonal | Curve |
| Center | Stop |

Pressing the button on `GP17` starts the melody. The melody plays while motor
control continues.

## Safety and troubleshooting

- The board resets when the motors start: check the motor power supply and
  connect a common ground.
- The motors do not respond: keep the joystick still during startup and check
  `GP26`/`GP27`.
- The LCD is not detected: run `i2c.scan()`. It should normally appear as
  `62` (`0x3E`).
- If `mpremote` reports that the port is busy, close the serial console in
  PyCharm or another program.

## License

> MIT License. Made with love and ducks by Rik, Arsenji, Benjamin, Grantly
> Marshall and Johannes Faizade.

**Greetings from Bavaria, Germany!**

_Thanks to the ZeFIx team, all the lovely mentors, and especially our mentor
Timo._
