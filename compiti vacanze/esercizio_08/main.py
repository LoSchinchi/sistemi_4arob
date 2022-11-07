#importiamo l'oggetto Pin e l'oggetto ADC dal modulo machine e la funzione sleep a nome sl dal modulo time
from machine import Pin, ADC
from time import sleep

#costanti della tensione, della frequenza e del valore di conversione
FREQ = 100
TENS = 3.3
CONVERSION_FACTOR = TENS / 2 ** 16

#vengono creati e istanziati il potenziometro e il led
pot = ADC(2)
led = Pin(0, Pin.OUT)

while True:
  #calcolo del valore del duty cicle
  duty_cicle = pot.read_u16() * CONVERSION_FACTOR / TENS * FREQ
  #accensione del led per duty cicle / FREQ sec
  led.value(1)
  sleep(duty_cicle / FREQ)
  #spegnimento del led per (differenza tra duty cicle massimo e DUTY_CICLE) / FREQ
  led.value(0)
  sleep((100 - duty_cicle) / FREQ)
