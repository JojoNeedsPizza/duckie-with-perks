from pynput import keyboard

class wheel_right:
 m1a = PWM(Pin(8)) #backward
 m1b = PWM(Pin(9)) #forward
 buzzer = PWM(Pin(22))

class wheel_left:
    m1a = PWM(Pin(10)) #backward
    m1b = PWM(Pin(11)) #forward
    buzzer = PWM(Pin(22))

def motor1_bewegen(geschwindigkeit):
    """
    Steuert Motor 1 mit einer Geschwindigkeit von -100 bis +100 Prozent.
    """
    # Wert auf den Bereich -100 bis 100 begrenzen
    geschwindigkeit = max(-100, min(100, geschwindigkeit))

    # Prozentwert in einen 16-Bit PWM-Wert (0 bis 65535) umrechnen
    pwm_wert = int(abs(geschwindigkeit) / 100 * 65535)

    if geschwindigkeit > 0:
        # Vorwärts drehen
        m1a.duty_u16(pwm_wert)
        m1b.duty_u16(0)
    elif geschwindigkeit < 0:
        # Rückwärts drehen
        m1a.duty_u16(0)
        m1b.duty_u16(pwm_wert)
    else:
        # Motor stoppen
        m1a.duty_u16(0)
        m1b.duty_u16(0)

def motor2_bewegen(geschwindigkeit):
    # Wert auf den Bereich -100 bis 100 begrenzen
    geschwindigkeit = max(-100, min(100, geschwindigkeit))

    # Prozentwert in einen 16-Bit PWM-Wert (0 bis 65535) umrechnen
    pwm_wert = int(abs(geschwindigkeit) / 100 * 65535)

    if geschwindigkeit > 0:
        # Vorwärts drehen
        m1a.duty_u16(pwm_wert)
        m1b.duty_u16(0)
    elif geschwindigkeit < 0:
        # Rückwärts drehen
        m1a.duty_u16(0)
        m1b.duty_u16(pwm_wert)
    else:
        # Motor stoppen
        m1a.duty_u16(0)
        m1b.duty_u16(0)
def forward():
    motor1_bewegen(100)
    motor2_bewegen(100)

def backward():
    motor1_bewegen(-100)




def on_press(key: keyboard.KeyCode):
    if key == keyboard.Key.esc:
        print("Escape key pressed. Exiting...")
    elif key == keyboard.Key.enter:
        print("Enter key pressed. Exiting...")

with keyboard.Listener(on_press=on_press) as listener:
            listener.join()