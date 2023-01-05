from turtle import *

nLati = int(input("lati: "))
L_LATI = 100

finestra = Screen()

finestra.title("scimmia")
finestra.bgcolor("lightblue")

alice = Turtle()
alice.color('white', 'pink')

alice.penup()
alice.goto(0, 250)
alice.pendown()
alice.pensize(5)
alice.begin_fill()
for k in range(nLati):
    alice.forward(L_LATI / nLati * 10)
    alice.right(360 / nLati)
alice.end_fill()

done()
