from machine import ADC, Pin, PWM
import time


# Grove 6
joystick_x = ADC(26)
joystick_y = ADC(27)

# Motor-Pins
m1a = PWM(Pin(8))
m1b = PWM(Pin(9))
m2a = PWM(Pin(10))
m2b = PWM(Pin(11))

for pwm in (m1a, m1b, m2a, m2b):
    pwm.freq(1000)

MITTE = 32768
DEADZONE = 7000
letzte_richtung = ""


def motor1_bewegen(geschwindigkeit):
    geschwindigkeit = max(-100, min(100, geschwindigkeit))
    pwm_wert = int(abs(geschwindigkeit) / 100 * 65535)

    if geschwindigkeit > 0:
        m1a.duty_u16(0)
        m1b.duty_u16(pwm_wert)
    elif geschwindigkeit < 0:
        m1a.duty_u16(pwm_wert)
        m1b.duty_u16(0)
    else:
        m1a.duty_u16(0)
        m1b.duty_u16(0)


def motor2_bewegen(geschwindigkeit):
    geschwindigkeit = max(-100, min(100, geschwindigkeit))
    pwm_wert = int(abs(geschwindigkeit) / 100 * 65535)

    if geschwindigkeit > 0:
        m2a.duty_u16(0)
        m2b.duty_u16(pwm_wert)
    elif geschwindigkeit < 0:
        m2a.duty_u16(pwm_wert)
        m2b.duty_u16(0)
    else:
        m2a.duty_u16(0)
        m2b.duty_u16(0)


def stoppen():
    motor1_bewegen(0)
    motor2_bewegen(0)


def richtung():
    x_wert = joystick_x.read_u16() - MITTE
    y_wert = joystick_y.read_u16() - MITTE

    links = x_wert > DEADZONE
    rechts = x_wert < -DEADZONE
    oben = y_wert < -DEADZONE
    unten = y_wert > DEADZONE

    if oben and links:
        return "oben-links"
    if oben and rechts:
        return "oben-rechts"
    if unten and links:
        return "unten-links"
    if unten and rechts:
        return "unten-rechts"
    if oben:
        return "oben"
    if unten:
        return "unten"
    if links:
        return "links"
    if rechts:
        return "rechts"
    return "mitte"


print("Joystick bereit: Grove 6")

try:
    while True:
        aktuelle_richtung = richtung()

        if aktuelle_richtung != letzte_richtung:
            print(aktuelle_richtung)
            letzte_richtung = aktuelle_richtung

        if aktuelle_richtung == "oben":
            motor1_bewegen(100)
            motor2_bewegen(100)
        elif aktuelle_richtung == "unten":
            motor1_bewegen(-100)
            motor2_bewegen(-100)
        elif aktuelle_richtung == "links":
            motor1_bewegen(-100)
            motor2_bewegen(100)
        elif aktuelle_richtung == "rechts":
            motor1_bewegen(100)
            motor2_bewegen(-100)
        else:
            stoppen()

        time.sleep_ms(50)
finally:
    stoppen()
    for pwm in (m1a, m1b, m2a, m2b):
        pwm.deinit()
