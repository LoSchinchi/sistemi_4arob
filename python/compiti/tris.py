from turtle import *

DIM_SEGNO = 100
N_CASELLE = 9
DIM_CASELLA = 200
SPESSORE_CAMPO = 30
COLORE_CAMPO = 'red'

screen = Screen()
screen.title('tris')

class Player:
    def __init__(self, nome, segno = 'x'):
        self.nome = nome
        self.segno = segno
        self.t = Turtle()

    def printSegno(self, x, y):
        self.t.penup()
        if self.segno == 'o':
            self.t.goto(x + DIM_SEGNO / 4, y - DIM_SEGNO)
        else:
            self.t.goto(x, y)
        self.t.pendown()
        self.t.begin_fill()

        if self.segno == 'x':
            for _ in range(4):
                self.t.right(45)
                self.t.forward(DIM_SEGNO * 2 / 5)
                self.t.left(90)
                self.t.forward(DIM_SEGNO * 2 / 5)
                self.t.right(90)
                self.t.forward(DIM_SEGNO / 5)
                self.t.right(45)
        else:
            self.t.circle(DIM_SEGNO / 2)
        self.t.end_fill()

    def isWinner(self, listOfCampo):
        for row in [listOfCampo[:3]] + [listOfCampo[3:-3]] + [listOfCampo[-3:]]:
            if row[0] == row[1] and row[0] == row[2] and row[0] == self.segno:
                return True

        for col in [listOfCampo[::3]] + [listOfCampo[1::3]] + [listOfCampo[2::3]]:
            if col[0] == col[1] and col[0] == col[2] and col[0] == self.segno:
                return True

        if listOfCampo[0] == listOfCampo[4] and listOfCampo[0] == listOfCampo[8] and listOfCampo[0] == self.segno:
            return True
            
        return listOfCampo[2] == listOfCampo[4] and listOfCampo[0] == listOfCampo[6] and listOfCampo[2] == self.segno
            
class Gioco:
    def __init__(self, g1, g2):
        self.listPos = [' '] * N_CASELLE
        self.listG = [g1, g2]
        self.t = Turtle()
        self.t.speed(0)
        self.t.color(COLORE_CAMPO, COLORE_CAMPO)
        self.setCoordCampo()
    
    def setCoordCampo(self):
        xC = -DIM_SEGNO / 2
        xS = -DIM_CASELLA - SPESSORE_CAMPO + xC
        xD = DIM_CASELLA + SPESSORE_CAMPO + xC
        yC = -xC
        yA = DIM_CASELLA + SPESSORE_CAMPO + yC
        yB = -DIM_CASELLA - SPESSORE_CAMPO + yC
        self.coordinate = [{'x': xS, 'y': yA}, {'x': xC, 'y': yA}, {'x': xD, 'y': yA}, 
                           {'x': xS, 'y': yC}, {'x': xC, 'y': yC}, {'x': xD, 'y': yC}, 
                           {'x': xS, 'y': yB}, {'x': xC, 'y': yB}, {'x': xD, 'y': yB}]
    
    def printCampo(self):
        for t in range(2):
            self.t.penup()
            self.t.goto(-DIM_CASELLA * 3 / 2 - SPESSORE_CAMPO, DIM_CASELLA / 2 + SPESSORE_CAMPO - (SPESSORE_CAMPO + DIM_CASELLA) * t)
            self.t.pendown()
            self.t.begin_fill()
            for _ in range(2):
                self.t.forward(DIM_CASELLA * 3 + SPESSORE_CAMPO * 2)
                self.t.right(90)
                self.t.forward(SPESSORE_CAMPO)
                self.t.right(90)
            self.t.end_fill()

            self.t.penup()
            self.t.goto(-DIM_CASELLA / 2 - SPESSORE_CAMPO + DIM_CASELLA * t, DIM_CASELLA * 3 / 2 + SPESSORE_CAMPO)
            self.t.pendown()
            self.t.begin_fill()
            for _ in range(2):
                self.t.forward(SPESSORE_CAMPO)
                self.t.right(90)
                self.t.forward(DIM_CASELLA * 3 + SPESSORE_CAMPO * 2)
                self.t.right(90)
            self.t.end_fill()
    
    def startGame(self):
        turno = 0
        while turno < 9 and not self.listG[0].isWinner(self.listPos) and not self.listG[1].isWinner(self.listPos):
            ind, indG = self.getIndPos(), int(turno % 2)
            x, y = self.coordinate[ind]['x'], self.coordinate[ind]['y']
            self.listPos[ind] = self.listG[indG].segno
            self.listG[indG].printSegno(x, y)
            turno += 1
        
        if self.listG[0].isWinner(self.listPos):
            print(f"complimenti {self.listG[0].nome}, hai vinto!!!")
        elif self.listG[1].isWinner(self.listPos):
            print(f"complimenti {self.listG[1].nome}, hai vinto!!!")
        else:
            print("la partita è finita in parità\n")
        
        s = input("volete giocare ancora? ")
        if s.lower() == 'si' or s.lower() == 'sì':
            self.listPos = [' '] * N_CASELLE
            self.listG = self.listG[::-1]
            screen.clear()
            self.printCampo()
            self.startGame()

    def getIndPos(self):
        lettPos1, lettPos2 = ['a', 'c', 'b'], ['s', 'c', 'd']
        string = input("inserisci la posizione sapendo le coordinate:\n- a -> alto\n- c -> centro\n- b -> basso\n- s -> sinistra\n- d -> destra\nposizione: ")
        
        if len(string) != 2:
            print("la stringa deve essere lunga due carattere")
            corr = False
        elif not string[0] in lettPos1:
            print(f"la prima lettera deve essere una tra {lettPos1}")
            corr = False
        elif not string[1] in lettPos2:
            print(f"la seconda lettera deve essere una tra {lettPos2}")
            corr = False
        else:
            corr = True
        ind = lettPos1.index(string[0]) * 3 + lettPos2.index(string[1])
        
        if self.listPos[ind] != ' ':
            print("posizione già occupata")
            return self.getIndPos()
        elif corr:
            return ind
        else:
            print("riscrivere la stringa!!")
            return self.getIndPos()


def main():
    n1 = input("nome giocatore 1: ")
    n2 = input("nome giocatore 2: ")
    g1 = Player(n1)
    g2 = Player(n2, 'o')

    gioco = Gioco(g1, g2)
    gioco.printCampo()
    gioco.startGame()

    done()


if __name__ == '__main__':
    main()