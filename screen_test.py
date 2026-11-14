from machine import I2C, Pin
from time import sleep_ms
from random import choice
from i2c_lcd import I2cLcd

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
lcd = I2cLcd(i2c, 0x3E, 2, 16)

SPRUECHE = (
    ("QUAK ATTACK!", "Duck mode: ON"),
    ("Duck you lookin", "at, feather?"),
    ("Quack happens.", "Stay fluffy."),
    ("Waddle I do?", "I drive!"),
    ("Egg-cellent!", "Mission started"),
    ("Feather power!", "Maximum quack"),
    ("No pond, no", "problem!"),
    ("Duck.exe", "is running"),
    ("Quack to the", "future!"),
    ("Flap engaged", "Hold on!"),
    ("Beware the", " mighty duck"),
    ("Too cool to", "beak-lieve"),
    ("Honk if you", "love ducks"),
    ("Duck side", "of the force"),
    ("Pond patrol", "reporting in"),
)


def zeile(text):
    """Gibt eine 16 Zeichen breite Zeile zentriert aus."""
    lcd.putstr(text[:16].center(16))


def lauftext(text, pause=90):
    """Schiebt einen längeren Text einmal von rechts nach links."""
    text = " " * 16 + text + " " * 16
    for position in range(len(text) - 15):
        lcd.clear()
        lcd.putstr(text[position:position + 16])
        sleep_ms(pause)


def quack_animation():
    for augen in ("^ ^", "o o", "- -", "o o"):
        lcd.clear()
        zeile("  (" + augen + ")")
        zeile("  >  V  <")
        sleep_ms(180)


def zeige_spruch():
    obere_zeile, untere_zeile = choice(SPRUECHE)
    lcd.clear()
    zeile(obere_zeile)
    zeile(untere_zeile)
    sleep_ms(900)
    lauftext(obere_zeile + "  " + untere_zeile)


while True:
    quack_animation()
    zeige_spruch()