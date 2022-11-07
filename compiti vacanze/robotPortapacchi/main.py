# importamo tutto da ir_rx.py e da motori.py e Pin dal modulo machine

from ir_rx import *
from motori import *
from machine import Pin

# valore del servo selezionato
valueServo = None

# funzione callback con data come parametro
def callback(data, addr, ctrl):
    # se c'è il dato
    if data > 0:
        # se il dato è riferito ad un motore, mettere il motore selezionato
        if data in servos:
           valueServo = data
        # muove il servo se c'è un servo selezionato e il valore serve per muoverlo
        if (data == VAL_AVANTI or data == VAL_INDIETRO) and valueServo is not None:
           servos[valueServo].moveServo(data)
        #muove i cingoli
        c1.moveCingolo(data)
        c2.moveCingolo(data)

#oggetti del sensore a infrarossi e dei cingolati
ir = Ir_rx(Pin(0, Pin.IN), callback)

c1 = Cingolato(0, 1, 162)
c2 = Cingolato(16, 17, 226)

#dictonary di servo data -> servo
servos = {
    48: Servo(2),
    24: Servo(3),
    122: Servo(4),
    16: Servo(5),
    56: Servo(6, 65, 100)
}
