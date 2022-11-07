"""
importiamo l'oggetto Pin e l'oggetto ADC dal modulo machine,
la funzione sleep dal modulo time e
il modulo _thred
"""
from machine import ADC, Pin
import _thread
from time import sleep

#costanti della tensione e del valore di conversione
TENS = 3.3
CONVERSION_FACTOR = TENS / 2 ** 16
#valore letto dal potenziometro, vale None se non ha ancora un valore dal potenziometro
val = None
#creazione del potenziometro
pot = ADC(2)

#il pin sarà 0 di default (quindi se non si inserisce alcun valore)
def core_1(pin=0):
#creazione del led
    led = Pin(pin, Pin.OUT)
    while True:
        #spegne il led e attende 0.5sec
        if val is None or val < 3.0:
            led.value(0)
            sleep(0.5)
        else:
            #il led si spege e si accende con 1sec di pausa
            led.value(0)
            sleep(1)
            led.value(1)
            sleep(1)

#viene creato un nuovo thread con heandler la funzione core_1
_thread.start_new_thread(core_1, ())
while True:
    #il valore di val viene aggiornato ogni secondo
    val = pot.read_u16() * CONVERSION_FACTOR
    sleep(1)
