from turtle import *
from time import sleep

dim = int(input("lato (in pixel): "))
finestra = Screen()

pensize(10)
finestra.title("indovina cos'è")
finestra.bgcolor("red")

penup()
goto(-dim / 6, dim / 2 - dim / 3)
pendown()
Screen().setup(width=.99, height=.99)

begin_fill()
for k in range(4):
    left(90)
    forward(dim / 3 * 2)
    right(90)
    forward(dim)
    right(90)
    forward(dim / 3)
    right(90)
    forward(dim / 3 * 2)
    left(90)
    forward(dim / 3)
end_fill()

pencolor('white')
goto(-dim / 6, dim / 2 - dim / 3)
for k in range(4):
    left(90)
    forward(dim / 3 * 2)
    right(90)
    forward(dim)
    right(90)
    forward(dim / 3)
    right(90)
    forward(dim / 3 * 2)
    left(90)
    forward(dim / 3)
hideturtle()

COLORS = ("blue", "orange", "yellow", "white", "lightblue", "grey", "green", "red", "purple", "pink", "magenta")

while True:
    for c in COLORS:
        Screen().bgcolor(c)
        sleep(0.15)
