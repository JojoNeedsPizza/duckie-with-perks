from machine import ADC, I2C, Pin, PWM
import time
from i2c_lcd import I2cLcd

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

# LCD JHD1803M1: SDA = GP4, SCL = GP5, Adresse = 0x3E
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100000)
lcd = I2cLcd(i2c, 0x3E, 2, 16)

MITTE = 32768
DEADZONE = 9000
MAX_SPEED = 100
current_motor1 = 0
current_motor2 = 0
letzte_richtung = ""
letzte_lcd_aktualisierung = 0
spruch_index = 0
animations_frame = 0

SPRUECHE = (
    ("QUAK ATTACK!", "Duck mode: ON"),
    ("Quack happens.", "Stay fluffy."),
    ("Waddle I do?", "I drive!"),
    ("Egg-cellent!", "Mission started"),
    ("Feather power!", "Maximum quack"),
    ("Duck.exe", "is running"),
    ("Quack to the", "future!"),
    ("Flap engaged", "Hold on!"),
    ("Pond patrol", "reporting in"),
)

MITTE = 32768
DEADZONE = 7000
letzte_richtung = ""

def ton(frequenz, dauer, lautstaerke=18000):
    buzzer.freq(frequenz)
    buzzer.duty_u16(lautstaerke)
    time.sleep_ms(dauer)
    buzzer.duty_u16(0)
    time.sleep_ms(25)

def silly_playful_sound():
    # "Ta-da!"
    ton(523, 100)
    ton(659, 100)
    ton(784, 180)

    # hüpfender Quietscher
    for frequenz in (900, 600, 1000, 500, 1200):
        ton(frequenz, 70)

    # lustiges Plopp
    for frequenz in range(700, 120, -40):
        ton(frequenz, 15, 14000)

    ton(180, 300, 22000)

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
            current_motor1 = min(current_motor1 + 10, motor1)
        elif current_motor1 > motor1:
            current_motor1 = max(current_motor1 - 10, motor1)

        if current_motor2 < motor2:
            current_motor2 = min(current_motor2 + 10, motor2)
        elif current_motor2 > motor2:
            current_motor2 = max(current_motor2 - 10, motor2)

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


def lcd_zeile(text):
    lcd.putstr(text[:16].center(16))


def startup_animation():
    for oben, unten in (
        ("      .--.", "     (o  o)"),
        ("     .--.  ", "    (o  o) "),
        ("    .--.   ", "   (o  o)  "),
        ("   .--.    ", "  (o  o)   "),
    ):
        lcd.clear()
        lcd_zeile(oben)
        lcd_zeile(unten)
        time.sleep_ms(180)

    for schritt in range(0, 17, 4):
        lcd.clear()
        lcd_zeile("DUCKIE BOOTING")
        lcd.move_to(0, 1)
        lcd.putstr(("=" * schritt + ">" + "." * 15)[:16])
        time.sleep_ms(120)


def lcd_animation(aktuelle_richtung):
    global letzte_lcd_aktualisierung, spruch_index, animations_frame

    jetzt = time.ticks_ms()
    if time.ticks_diff(jetzt, letzte_lcd_aktualisierung) < 500:
        return

    letzte_lcd_aktualisierung = jetzt
    animations_frame = (animations_frame + 1) % 4
    spruch_oben, spruch_unten = SPRUECHE[spruch_index]
    lcd.clear()

    if animations_frame == 0:
        lcd_zeile("  (^ ^)  QUAK")
        lcd_zeile(aktuelle_richtung)
    elif animations_frame == 1:
        lcd_zeile("  (o o)  QUAK")
        lcd_zeile(spruch_oben)
    elif animations_frame == 2:
        lcd_zeile("  (- -)  QUAK")
        lcd_zeile(spruch_unten)
    else:
        lcd_zeile("  (o o)  QUAK")
        lcd_zeile(aktuelle_richtung)
        spruch_index = (spruch_index + 1) % len(SPRUECHE)


def richtung():
    x_wert = sum(joystick_x.read_u16() for _ in range(4)) // 4 - MITTE
    y_wert = sum(joystick_y.read_u16() for _ in range(4)) // 4 - MITTE

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
startup_animation()
lcd.clear()
lcd_zeile("DUCKIE ONLINE")
lcd_zeile("QUAK QUAK!")
time.sleep_ms(800)

try:
    while True:
        aktuelle_richtung = richtung()
        fahre(aktuelle_richtung)
        lcd_animation(aktuelle_richtung)

        if aktuelle_richtung != letzte_richtung:
            print("Richtung:", aktuelle_richtung)
            letzte_richtung = aktuelle_richtung

        time.sleep_ms(50)
finally:
    stoppen()
    for pwm in (m1a, m1b, m2a, m2b):
        pwm.deinit()
    buzzer.deinit()

# jojoneedspizza, like frrrr :)