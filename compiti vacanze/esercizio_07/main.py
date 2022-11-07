#importiamo l'oggetto Pin dal modulo machine e la funzione sleep dal modulo time
from machine import Pin
from time import sleep

"""
costanti della frequenza e del duty cicle
(34 -> il led rimarrà acceso 0.34 sec)
"""
FREQ = 100
DUTY_CICLE = 34

#creazione del led tramite un oggetto Pin
led = Pin(0, Pin.OUT)

while True:
  #accensione del led per DUTY_CICLE / FREQ sec
  led.value(1)
  sleep(DUTY_CICLE / FREQ)
  #spegnimento del led per (differenza tra duty cicle massimo e DUTY_CICLE) / FREQ
  led.value(0)
  sleep((100 - DUTY_CICLE) / FREQ)
