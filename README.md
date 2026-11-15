# Duckie with Perks




**Written in** 



A small remote-controlled vehicle based on the **Maker Pi RP2040**. Duckie is
controlled with an analog joystick and has additional perks:

- Differential drive with two motors
- Joystick control, including diagonal directions
- JHD1803M1 I²C LCD with duck animations and catchphrases
- Startup sound and a non-blocking “Alle meine Entchen” melody
- Button-triggered melody playback
- Smooth acceleration and a safety stop

## Infos about the Hackathon where it got created

> **ZeFIx 2026**

**Name:**  ZeFIx 2026

**Date:**  13.11.2026 - 15.11.2026

**Team:**  Benjamin, Grantly Marshall, Arsenji, Rik and Johannes Faizade

**Challenge:**  Classic Duckies are boooring, we gotta give them sum features

**Our contribution:**  A car for bathing ducks, that can drive, say quack on an display and play the german song "Alle meine Entchen" when a button is pressed. It also has a startup sound and smooth acceleration.

**Result / placement:**  Duckie with Perks :).

-- Imma add the Image on github later --

## Hardware

- Maker Pi RP2040
- Two DC motors with wheels
- Analog joystick module, such as the HW-505
- JHD1803M1 I²C LCD
- Push button
- 1 AAA battery slot and 2 AA battery slots

Do not power the motors from the RP2040's 3.3 V output. The motor power
supply and the board must share a common ground (`GND`).

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
input `LOW` when the button is pressed.

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

| Joystick direction | Behavior |
|---|---|
| Up | Forward |
| Down | Reverse |
| Left / right | Turn |
| Diagonal | Curve |
| Center position | Stop |

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

## Lizenz

> **MIT License, Made with Luv and Ducks by: Rik, Arsenji, Benjamin, Grantly Marshall and Johannes Faizade**

**Greetings from Bavaria, Germany!**

 *Thanks to the ZeFix team, all the nice mentors and especially our mentor Timo*
