from turtle import *

nLati = int(input("lati: "))
L_LATI = 100

Screen().title("scimmia")
Screen().bgcolor("lightblue")
pencolor("gold")

penup()
goto(0, 250)
pendown()
pensize(5)

for k in range(nLati):
    forward(L_LATI / nLati * 10)
    right(360 / nLati)

done()
