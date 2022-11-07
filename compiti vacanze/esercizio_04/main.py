#importiamo l'oggetto Pin dal modulo machine e la funzione sleep dal modulo time
from machine import Pin
from time import sleep

#creazione del led tramite un oggetto Pin di output
led = Pin(25, Pin.OUT)
#creazione e istanziamento del bottone, che sarà un pin di input di pull up
bot = Pin(0, Pin.IN, Pin.PULL_UP)

while True:
  #se il pulsante è premuto accende il led per mezzo secondo
  if not bot.value():
    led.value(1)
    sleep(0.5)
  led.value(0)
  sleep(0.15)
