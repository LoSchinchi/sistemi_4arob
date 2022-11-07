#importiamo l'oggetto Pin dal modulo machine e la funzione sleep dal modulo time
from machine import Pin
from time import sleep

#pin del led di sistema
LED_DEFAULT = 25

#creazione del led tramite un oggetto Pin, tra parentesi il pin e se è di input o output
led = Pin(LED_DEFAULT, Pin.OUT)

#ciclo infinito
while True:
  led.toggle()
  sleep(1)
  #cambia il valore del led (0 o 1) ogni secondo
