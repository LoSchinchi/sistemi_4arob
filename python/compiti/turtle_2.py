from turtle import *

L_LATI = 500
MIN_LATI = 3
N_POLIG = 9
START_X = -700
START_Y = 500

def drawTurtle(t, x, y, nLati, color):
    t.pensize(10)
    t.penup()
    t.goto(x, y)
    t.color('gold', color)
    t.pendown()
    t.begin_fill()
    for _ in range(nLati):
        t.forward(L_LATI * 2 / nLati)
        t.right(360 / nLati)
    t.end_fill()

def main():
    listTurtle = [Turtle() for _ in range(N_POLIG)]
    list_x = [START_X, 0, -START_X] * 3
    list_y = [START_Y] * 3 + [0] * 3 + [-START_Y] * 3
    list_n_lati = [n + MIN_LATI for n in range(N_POLIG)]
    listColori = ['black', 'green', 'white', 'red', 'yellow', 'orange', 'blue', 'pink', 'lightblue']

    for t, x, y, l, c in zip(listTurtle, list_x, list_y, list_n_lati, listColori):
        drawTurtle(t, x, y, l, c)
    done()

if __name__ == '__main__':
    main()