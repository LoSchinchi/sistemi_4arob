#importiamo l'oggetto Pin dal modulo machine e la funzione sleep dal modulo time
from machine import Pin
from time import sleep

#creazione del led tramite un oggetto Pin di output, il primo parametro è il pin del led
led = Pin(0, Pin.OUT)

while True:
  led.value(1)
  print("Ciao, Mondo!")
  sleep(0.5)
  led.value(0)
  sleep(0.5)
  #si accende il led per mezzo secondo e stampa 'Ciao, Mondo!', poi lo spegne per mezzo secondo
