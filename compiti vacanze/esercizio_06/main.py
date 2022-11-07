#importiamo l'oggetto Pin e l'oggetto ADC dal modulo machine e la funzione sleep a nome sl dal modulo time
from machine import Pin, ADC
from time import sleep as sl

#costanti della tensione del valore di conversione, ** è l'elevamento a potenza
TENS = 3.3
CONVERSION_FACTOR = TENS / 2 ** 16

#tupla con i pin dei led e array di led inizialmente vuoto
pinLed = (0, 1, 12, 13, 15, 14, 10, 5, 7)
led = []

#aggiungiamo all'array dei led con pin i valori della tupla
for p in pinLed:
  led.append(Pin(p, Pin.OUT))
#istanziamo il pin del potenziometro
pot = ADC(2)
#calcolo del valore che il potenziometro deve assumere per accendere un led
valLed = (TENS - 0.1) / len(pinLed)

while True:
  #lettura del valore analogico convertito e diviso per valLed per sapere quanti led si devono accendere
  v = pot.read_u16() * CONVERSION_FACTOR / valLed
  #accensione dei primi v led
  for n in range(len(pinLed)):
    if n <= v:
      led[n].value(1)
    else:
      led[n].value(0)
