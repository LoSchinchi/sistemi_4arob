#importiamo l'oggetto Pin dal modulo machine e la funzione sleep a nome sl dal modulo time
from machine import Pin
from time import sleep as sl

#vengono creati e istanziati i 3 led del semaforo
ledRosso = Pin(0, Pin.OUT)
ledGiallo = Pin(1, Pin.OUT)
ledVerde = Pin(2, Pin.OUT)

#creazione e istanziamento del bottone, che sarà un pin di input di pull up
bot = Pin(15, Pin.IN, Pin.PULL_UP)

while True:
  if not bot.value():
    """ se il pulsante è premuto accende il led rosso per 2 sec, poi lo spegne e accende quello verde per 2 sec,
        infine spegne il led verde e accende quello giallo per mezzo sec prima di spegnerlo """
    ledRosso.value(1)
    sl(2)
    ledRosso.value(0)
    ledVerde.value(1)
    sl(2)
    ledGiallo.value(1)
    ledVerde.value(0)
    sl(0.5)
    ledGiallo.value(0)
  else:
    #altrimenti il led lampeggia 2 volte in 0.7 sec
    ledGiallo.value(1)
    sl(0.35)
    ledGiallo.value(0)
    sl(0.35)
