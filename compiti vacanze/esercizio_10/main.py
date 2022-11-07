"""
importiamo l'oggetto Pin e l'oggetto ADC dal modulo machine,
la funzione sleep dal modulo time e
il modulo _thred
"""
from machine import ADC, Pin
import _thread
from time import sleep

binarioColori ={ 0: 126,    # 1111110
                 1: 48,     # 110000
                 2: 109,    # 1101101
                 3: 121,    # 1111001
                 4: 51,     # 110011
                 5: 91,     # 1011011
                 6: 95,     # 1011111
                 7: 112,    # 1110000
                 8: 127,    # 1111111
                 9: 123     # 1111011
}
#tupla con i pin dei led
pinLed = (0, 4, 11, 16, 17, 18, 19)

#costanti della tensione, dell'intervallo tra i led e del valore di conversione
TENS = 3.3
INTERVALLO = TENS / len(binarioColori)
CONVERSION_FACTOR = TENS / 2 ** 16

#array con i led e il valore del potenziometro (inizialmente None)
leds = []
valore = None

def printLed():
  # v è il numero decimale del numero binario corrispondente a led da accendere in quel momento
  v = binarioColori[valore // INTERVALLO]

  # accensione dei led del display in base a v, che verrà dimezzato ogni volta
  for k in range(len(pinLed) - 1, 0, -1):
    leds[k].value(v % 2)
    v = v // 2

def core_1():
  while True:
    if valore is not None:
      printLed()
      sleep(0.5)

# ad ogni ciclo viene aggiunto un led del display in base al pin
# viene creato ed istanziato anche il potenziometro
for pin in pinLed:
  leds.append(Pin(pin, Pin.OUT))
pot = ADC(2)

#viene creato un nuovo thread con heandler la funzione core_1
_thread.start_new_thread(core_1, ())
while True:
  # la variabile valore assume il valore del potenziometro convertito ogni 0.5sec
  valore = pot.read_u16() * CONVERSION_FACTOR
  sleep(0.5)
