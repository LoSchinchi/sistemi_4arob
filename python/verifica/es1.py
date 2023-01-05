from turtle import *

DIM_X_BARRA = 4
DIM_Y_BARRA = 100
SPAZIO = 1

def setBin(c):
    s = bin(ord(c))[2:]  # prende la stringa senza lo 0b
    return '0' * (8 - len(s)) + s  # ritorna con gli 0 davanti

"""
 classe Barcode:
 ha l'__init__ che riceve come parametro una stringa
 ha il metodo printCode che stampa il codice a barre mediante la libreria turtle  
"""
class Barcode:
    def __init__(self, stringa):
        self.strCod = ''.join([setBin(c) for c in stringa])  # ho usato join per unire già tutti i caratteri # decodificati
        self.t = Turtle()   # inizializzazione turtle dell'oggetto
        self.t.pensize(DIM_X_BARRA)
        self.t.right(90)
        self.t.hideturtle()
        self.t.speed(0)

    def printCode(self):
        xAtt = 0
        for bit in self.strCod:
            if bit == '1':
                self.t.color("black", "black")  # se è 1 barra nera, altrimenti bianca
            else:
                self.t.color("white", "white")
            self.t.penup()
            self.t.goto(xAtt, 0)
            self.t.pendown()
            self.t.forward(DIM_Y_BARRA)
            xAtt += DIM_X_BARRA + SPAZIO # incrementa la x della riga successiva


def main():
    while True:
        s = input("inserisci una stringa di 8 caratteri: ")
        if not s.isascii():  # controllo codice ascii
            print("la stringa deve contenere solo codici asci")
            continue
        elif len(s) == 8:  # controllo lunghezza
            break
        print("la stringa non è lunga 8 caratteri")

    b = Barcode(s)
    b.printCode()
    done()


if __name__ == '__main__':
    main()
