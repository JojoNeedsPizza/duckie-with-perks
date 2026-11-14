from machine import ADC
import time

x = ADC(26)  # Grove 6A
y = ADC(27)  # Grove 6B

MITTE = 32768
DEADZONE = 7000
letzte_richtung = ""


def richtung():
    x_wert = x.read_u16() - MITTE
    y_wert = y.read_u16() - MITTE

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


while True:
    aktuelle_richtung = richtung()

    if aktuelle_richtung != letzte_richtung:
        print(aktuelle_richtung)
        letzte_richtung = aktuelle_richtung

    time.sleep_ms(50)