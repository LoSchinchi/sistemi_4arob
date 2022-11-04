from turtle import *

lati = int(input("lati: "))
L_LATI = 100

Screen().title("scimmia")
Screen().bgcolor("lightblue")

color('black', 'yellow')
#begin_fill()

penup()
goto(0, L_LATI)
pendown()
pensize(5)

for k in range(lati):
    forward(L_LATI)
    left(360 * 3 / lati)

#end_fill()
done()