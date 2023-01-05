from turtle import *
from time import sleep

def palla(x):
    setheading(360)
    penup()
    goto(x, -DIMENSIONE / 2 - RAGGIO)
    pendown()
    circle(RAGGIO)

def pallaColorata(x):
    begin_fill()
    palla(x)
    end_fill()

def rettangolo():
    penup()
    goto(-RAGGIO, -DIMENSIONE / 2 + RAGGIO)
    pendown()
    left(90)
    forward(DIMENSIONE)
    right(90)
    forward(RAGGIO * 2)
    right(90)
    forward(DIMENSIONE)

def rettangoloColorato():
    begin_fill()
    rettangolo()
    end_fill()

def semicerchioColorato():
    begin_fill()
    penup()
    goto(RAGGIO, DIMENSIONE / 2 + RAGGIO)
    setheading(90)
    pendown()
    circle(RAGGIO, 180)
    end_fill()

def lineaSopra():
    penup()
    goto(0, DIMENSIONE / 2 + RAGGIO * 5 / 3)
    right(180)
    pendown()
    forward(RAGGIO / 3)

dizCol = {"bianco": "pink", "nero": "black"}

DIMENSIONE = int(input("centimetri: ")) * 30
RAGGIO = int(input("Raggio della palla (in pixel): "))
c =dizCol[input("colore (bianco o nero): ")]
color(c)
if c == "pink":
    pencolor("black")
else:
    pencolor("white")

pensize(10)
Screen().bgcolor("lightblue")
Screen().title("DICK")

pallaColorata(-RAGGIO)
pallaColorata(RAGGIO)
rettangoloColorato()
semicerchioColorato()
palla(-RAGGIO)
palla(RAGGIO)
rettangolo()
lineaSopra()
hideturtle()


COLORS = ("blue", "orange", "yellow", "white", "lightblue", "grey", "green", "red", "purple", "magenta")
while True:
    for c in COLORS:
        Screen().bgcolor(c)
        sleep(0.15)

