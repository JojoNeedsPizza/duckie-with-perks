from machine import ADC, Pin, PWM
import time

# Motoren
m1a = PWM(Pin(8))
m1b = PWM(Pin(9))
m2a = PWM(Pin(10))
m2b = PWM(Pin(11))
buzzer = PWM(Pin(22))

for pwm in (m1a, m1b, m2a, m2b):
    pwm.freq(1000)


# Joystick an Grove 6
joystick_x = ADC(26)
joystick_y = ADC(27)

MITTE = 32768
DEADZONE = 7000
MAX_SPEED = 45
current_motor1 = 0
current_motor2 = 0
letzte_richtung = ""


def motor1_bewegen(geschwindigkeit):
    geschwindigkeit = max(-100, min(100, geschwindigkeit))
    pwm_wert = int(abs(geschwindigkeit) * 65535 / 100)

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
    pwm_wert = int(abs(geschwindigkeit) * 65535 / 100)

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


def motoren_setzen(motor1, motor2):
    global current_motor1, current_motor2

    motor1 = max(-MAX_SPEED, min(MAX_SPEED, motor1))
    motor2 = max(-MAX_SPEED, min(MAX_SPEED, motor2))

    # Kleine Schritte verhindern einen abrupten Stromanstieg.
    while current_motor1 != motor1 or current_motor2 != motor2:
        if current_motor1 < motor1:
            current_motor1 = min(current_motor1 + 5, motor1)
        elif current_motor1 > motor1:
            current_motor1 = max(current_motor1 - 5, motor1)

        if current_motor2 < motor2:
            current_motor2 = min(current_motor2 + 5, motor2)
        elif current_motor2 > motor2:
            current_motor2 = max(current_motor2 - 5, motor2)

        motor1_bewegen(current_motor1)
        motor2_bewegen(current_motor2)
        time.sleep_ms(5)


def ton(frequenz, dauer, lautstaerke=18000):
    buzzer.freq(frequenz)
    buzzer.duty_u16(lautstaerke)
    time.sleep_ms(dauer)
    buzzer.duty_u16(0)
    time.sleep_ms(25)


def startup_sound():
    # Silly playful duck startup sound
    for frequenz, dauer in (
        (523, 100),
        (659, 100),
        (784, 180),
        (900, 70),
        (600, 70),
        (1000, 70),
        (500, 70),
        (1200, 100),
    ):
        ton(frequenz, dauer)

    for frequenz in range(700, 120, -40):
        ton(frequenz, 15, 14000)

    ton(180, 300, 22000)


def richtung():
    x_wert = joystick_x.read_u16() - MITTE
    y_wert = joystick_y.read_u16() - MITTE

    # Links und rechts sind absichtlich vertauscht.
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


def fahre(aktuelle_richtung):
    if aktuelle_richtung == "oben":
        motoren_setzen(MAX_SPEED, MAX_SPEED)
    elif aktuelle_richtung == "oben-rechts":
        motoren_setzen(MAX_SPEED, 20)
    elif aktuelle_richtung == "oben-links":
        motoren_setzen(20, MAX_SPEED)
    elif aktuelle_richtung == "unten":
        motoren_setzen(-MAX_SPEED, -MAX_SPEED)
    elif aktuelle_richtung == "unten-rechts":
        motoren_setzen(-MAX_SPEED, -20)
    elif aktuelle_richtung == "unten-links":
        motoren_setzen(-20, -MAX_SPEED)
    elif aktuelle_richtung == "rechts":
        motoren_setzen(MAX_SPEED, -MAX_SPEED)
    elif aktuelle_richtung == "links":
        motoren_setzen(-MAX_SPEED, MAX_SPEED)
    else:
        motoren_setzen(0, 0)


print("Duckie bereit!")
startup_sound()

try:
    while True:
        aktuelle_richtung = richtung()
        fahre(aktuelle_richtung)

        if aktuelle_richtung != letzte_richtung:
            print("Richtung:", aktuelle_richtung)
            letzte_richtung = aktuelle_richtung

        time.sleep_ms(50)
finally:
    stoppen()
    for pwm in (m1a, m1b, m2a, m2b):
        pwm.deinit()
    buzzer.deinit()
