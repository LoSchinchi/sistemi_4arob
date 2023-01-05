from turtle import *
from time import sleep
from random import randint

ID_MOD_MORTALE = 1
ID_MOD_IMMORTALE = 2
COLOR_SNAKE = "lightblue"
COLOR_CIBO = "green"
DIM_PUNTO_SNAKE = 70
N_PUNTI_PER_RIGA = 10
DIM_X = DIM_PUNTO_SNAKE * N_PUNTI_PER_RIGA
DIM_Y = DIM_X
COLOR_BORDERS = "black"
SIZE_BORDERS = 20

def setTipoGioco():
    print("Modalità:")
    print(f"{ID_MOD_MORTALE} -> mortale: non puoi colpire te stesso o le pareti")
    print(f"{ID_MOD_IMMORTALE} -> immortale: passi attraverso le pareti, puoi colpirti ma perderai lunghezza")

    answer = int(input("modalità scelta: "))
    if answer != ID_MOD_MORTALE and answer != ID_MOD_IMMORTALE:
        print("modalità non presente!!")
        return setTipoGioco()
    else:
        return answer

def setCampoGioco(screen):
    screen.title("snake")
    t = Turtle()
    t.hideturtle()
    t.color(COLOR_BORDERS, COLOR_BORDERS)
    t.speed(0)

    t.penup()
    t.goto(-DIM_X / 2 - SIZE_BORDERS, DIM_Y / 2 + SIZE_BORDERS)
    t.pendown()
    t.begin_fill()
    for _ in range(4):
        t.forward(DIM_X + SIZE_BORDERS * 2)
        t.right(90)

    t.penup()
    t.goto(-DIM_X / 2, DIM_Y / 2)
    t.pendown()
    for _ in range(4):
        t.forward(DIM_X)
        t.right(90)
    t.end_fill()

def indexOfPuntoInSnake(_list, x, y):
    for i, p in enumerate(_list):
        if p.x == x and p.y == y:
            return i
    return -1

class Punto:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

        self.t = Turtle()
        self.t.speed(0)
        self.t.color(COLOR_SNAKE, COLOR_SNAKE)
        self.t.hideturtle()

    def printPunto(self):
        self.t.begin_fill()
        self.t.penup()
        self.t.goto(self.x + 10, self.y - 10)
        self.t.pendown()
        for _ in range(4):
            self.t.forward(DIM_PUNTO_SNAKE - 20)
            self.t.right(90)
        self.t.end_fill()

    def hidePunto(self):
        self.t.clear()

    def isLatoToccato(self):
        x, y = self.x, self.y
        return x < -DIM_X / 2 or x > DIM_X / 2 - DIM_PUNTO_SNAKE or y > DIM_Y / 2 or y < -DIM_Y / 2 + DIM_PUNTO_SNAKE

    def setCibo(self, snake):
        while True:
            x = randint(0, N_PUNTI_PER_RIGA - 1) * DIM_PUNTO_SNAKE - DIM_X / 2
            y = randint(0, N_PUNTI_PER_RIGA - 1) * -DIM_PUNTO_SNAKE + DIM_Y / 2
            if indexOfPuntoInSnake(snake.punti, x, y) == -1:
                break
        self.x = x
        self.y = y
        self.t.color(COLOR_CIBO, COLOR_CIBO)
        self.printCibo()

    def printCibo(self):
        self.t.begin_fill()
        self.t.penup()
        self.t.goto(self.x + 20, self.y - 20)
        self.t.pendown()
        for _ in range(4):
            self.t.forward(DIM_PUNTO_SNAKE - 40)
            self.t.right(90)
        self.t.end_fill()


class Snake:
    def __init__(self, mod):
        self.mod = mod
        self.direz = "destra"
        self.t = Turtle()
        self.punti = [Punto(0, 0), Punto(-DIM_PUNTO_SNAKE, 0)]
        self.punti[0].printPunto()
        self.punti[1].printPunto()

    def changhePosToRight(self):
        if self.direz != "sinistra":
            self.direz = "destra"

    def changhePosToUp(self):
        if self.direz != "giu":
            self.direz = "su"

    def changhePosToDown(self):
        if self.direz != "su":
            self.direz = "giu"

    def changhePosToLeft(self):
        if self.direz != "destra":
            self.direz = "sinistra"

    def startGame(self):
        cibo = Punto()
        cibo.setCibo(self)

        while True:
            ultimo = self.punti.pop()
            ultimo.hidePunto()

            newHead = Punto(self.punti[0].x, self.punti[0].y)
            if self.direz == "destra":
                newHead.x = newHead.x + DIM_PUNTO_SNAKE
            elif self.direz == "sinistra":
                newHead.x = newHead.x - DIM_PUNTO_SNAKE
            elif self.direz == "su":
                newHead.y = newHead.y + DIM_PUNTO_SNAKE
            else:
                newHead.y = newHead.y - DIM_PUNTO_SNAKE

            if newHead.isLatoToccato():
                if self.mod == ID_MOD_MORTALE:
                    break
                elif self.direz == "destra":
                    newHead.x = -DIM_X / 2
                elif self.direz == "sinistra":
                    newHead.x = DIM_X / 2 - DIM_PUNTO_SNAKE
                elif self.direz == "su":
                    newHead.y = -DIM_Y / 2 + DIM_PUNTO_SNAKE
                else:
                    newHead.y = DIM_Y / 2
            newHead.printPunto()

            if cibo.x == newHead.x and cibo.y == newHead.y:
                cibo.hidePunto()
                ultimo.printPunto()
                self.punti.append(ultimo)
                cibo.setCibo(self)

            ind = indexOfPuntoInSnake(self.punti, newHead.x, newHead.y)
            if ind != -1:
                if self.mod == ID_MOD_MORTALE:
                    break
                else:
                    for p in self.punti[ind:]:
                        p.hidePunto()
                    self.punti = self.punti[:ind]

            self.punti = [newHead] + self.punti
            if self.mod == ID_MOD_MORTALE:
                sleep(0.1)
            else:
                sleep(1 / len(self.punti))

    def endGame(self,):
        for p in self.punti:
            p.hidePunto()
            sleep(0.5)


def main():
    screen = Screen()
    hideturtle()

    mod = setTipoGioco()
    setCampoGioco(screen)

    snake = Snake(mod)
    onkey(snake.changhePosToRight, "Right")
    onkey(snake.changhePosToUp, "Up")
    onkey(snake.changhePosToDown, "Down")
    onkey(snake.changhePosToLeft, "Left")
    listen()

    snake.startGame()
    snake.endGame()
    print("fine partita")
    done()


if __name__ == '__main__':
    main()
