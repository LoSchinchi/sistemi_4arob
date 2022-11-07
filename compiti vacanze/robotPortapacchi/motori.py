from machine import Pin, PWM

DATA_AVANTI = 2
DATA_INDIETRO = 152

class Cingolato:

  def __init__(self, pin1, pin2, vStop):
    self.pinAvanti = pin1
    self.pinIndietro = pin2
    self.stop = vStop
    self.direzione = None

  def setDirezione(self, val):
    if val == self.stop:
      self.direzione = None
    elif val == DATA_AVANTI:
      self.direzione = 0
    elif val == DATA_INDIETRO:
      self.direzione = 1
  
  def moveCingolo(self, val):
    setDirezione(self, val)

    if self.direzione is None:
      self.pinAvanti.value(0)
      self.pinIndietro.value(0)
    elif self.direzione == 0:
      self.pinAvanti.value(1)
      self.pinIndietro.value(0)
    else:
      self.pinAvanti.value(0)
      self.pinIndietro.value(1)


MIN_GRADI = 0
MAX_GRADI = 180
DUTY_0_GRADI = 1000
DUTY_180_GRADI = 20000
DUTY_PER_GRADO = (DUTY_180_GRADI - DUTY_0_GRADI) / (MAX_GRADI - MIN_GRADI)
VAL_AVANTI = 144
VAL_INDIETRO = 244
INTERVALLO_GRADI = 3

class Servo:

  def __init__(self, pin, min_g=MIN_GRADI, max_g=MAX_GRADI, fr=100):
    self.pwm = PWM(Pin(pin))
    self.pwm.freq(fr)

    self.MIN_G = min_g
    self.MAX_G = max_g
    self.posiz = (min_g + max_g) // 2

  def getDuty(self):
    return DUTY_PER_GRADO * self.posiz
  
  def moveServo(self, val):
    self.setPosiz(val)
    self.pwm.duty_u16(self.getDuty(self))
    
  def setPosiz(self, val):
    if val == VAL_AVANTI:
      self.posiz = self.posiz + INTERVALLO_GRADI if self.posiz < self.MAX_G - INTERVALLO_GRADI else self.MAX_G
    elif val == VAL_INDIETRO:
      self.posiz = self.posiz - INTERVALLO_GRADI if self.posiz > INTERVALLO_GRADI + self.MIN_G else self.MIN_G
    