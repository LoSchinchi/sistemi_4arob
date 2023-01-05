

from turtle import *
from time import sleep

COLORS = ("blue", "orange", "yellow", "white", "lightblue", "grey", "green", "red", "purple", "pink", "magenta")
DIM = 350
ANGOLO = 30

window = Screen()
window.title("adolfo")

t = Turtle()
t.speed(0)
t.fillcolor("black")
ang_att = 0

while True:
    goto(0, 0)
    t.begin_fill()
    t.right(ang_att % 360)
    for k in range(4):
        t.left(90)
        t.forward(DIM / 3 * 2)
        t.right(90)
        t.forward(DIM)
        t.right(90)
        t.forward(DIM / 3)
        t.right(90)
        t.forward(DIM / 3 * 2)
        t.left(90)
        t.forward(DIM / 3)
    t.end_fill()
    sleep(1)
    t.clear()
    ang_att += ANGOLO