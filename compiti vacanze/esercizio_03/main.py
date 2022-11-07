#importiamo l'oggetto Pin dal modulo machine e la funzione sleep a nome sl dal modulo time
from machine import Pin
from time import sleep as sl

#vengono creati e istanziati i 3 led del semaforo
ledRosso = Pin(0, Pin.OUT)
ledGiallo = Pin(1, Pin.OUT)
ledVerde = Pin(2, Pin.OUT)

while True:
  #sarà sempre vero
  if True:
    """ accende il led rosso per 2 sec, poi lo spegne e accende quello verde per 2 sec,
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
    #per otto volte alterna il valore del led giallo (o 0 o 1) e attende per 0.35 sec
    for k in range(8):
      ledGiallo.toggle()
      sl(0.35)
