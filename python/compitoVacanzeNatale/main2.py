"""import pgzero, pgzrun, pygame
import math, sys, random
from enum import Enum
from time import sleep

WIDTH = 1577
HEIGHT = 682
TITLE = 'Basketball 3 v 3'


class Ball(Actor):
    def __init__(self):
        super().__init__('ball', (0, 0))


class Game:
    def draw(self):
        screen.blit('campo', (0, 0))


def draw():
    g.draw()


try:
    pygame.mixer.quit()
    pygame.mixer.init(44100, -16, 2, 1024)
except Exception:
    pass

g = Game()
pgzrun.go()"""
import math
import pygame
import numpy as np
import sys
from pygame.locals import *

WIDTH = 1577
HEIGHT = 682
TITLE = 'Basketball 3 v 3'
FPS = 50
SIZE_BALL = (40, 40)
COORD_CANESTRO_1 = (250, 105)
COORD_CANESTRO_2 = {'x': WIDTH - 250 - SIZE_BALL[0], 'y': 202, 'z': HEIGHT - 307}
#COORD_FERRO_CANESTRO_2 = (COORD_CANESTRO_2[0] - 40, COORD_CANESTRO_2[1])
COORD_FERRO_CANESTRO_2 = {'x': COORD_CANESTRO_2['x'] - 40, 'y': 202, 'z': HEIGHT - 307}
X_CAMPO = 1433
Y_CAMPO = 245
Y_BORDO_2_CAMPO = 47


class Game:
    def __init__(self):
        self.display = None
        self.imgCampo = pygame.image.load('images/campo.png')
        self.setupWindow()
        self.ball = Ball()
        self.team_1 = Team(1)

    def setupWindow(self):
        self.display = pygame.display.set_mode(self.imgCampo.get_size())
        pygame.display.set_caption(TITLE)
        self.showImage(self.imgCampo, 0, 0)

    def showImage(self, img, x, y):
        self.display.blit(img, (x, y))

    def reloadWindow(self):
        self.showImage(self.imgCampo, 0, 0)
        #self.showImage(self.team_1.imgBarraTiro, WIDTH - 250 - SIZE_BALL[0], HEIGHT - COORD_CANESTRO_2['y'] - COORD_CANESTRO_2['z'])
        #return
        self.team_1.writeBarraTiro(self.ball, self.display)

        self.ball.movPalla()
        self.display.blit(self.ball.imgBall, self.ball.coordToDraw())

        for p in self.team_1.players:
            p.updatePlayer(self.ball, self.team_1.attackTo)
            if not p.selected:
                if p.x < self.ball.x:
                    p.drawPlayer(self.display, 'right', self.team_1.imgTriangle)
                else:
                    p.drawPlayer(self.display, 'left', self.team_1.imgTriangle)
            else:
                p.drawPlayer(self.display, self.team_1.attackTo, self.team_1.imgTriangle)

    def checkMovimentiTeam_2(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.team_1.attackTo = 'left'
            for g in self.team_1.players:
                if g.selected and g.x > self.__calcoloCateto(g.y) - 30 and not g.inSalto and g.z == 0:
                    g.x -= 15
                    break
        if keys[pygame.K_RIGHT]:
            self.team_1.attackTo = 'right'
            for g in self.team_1.players:
                if g.selected and g.x < WIDTH - self.__calcoloCateto(g.y) - 140 and not g.inSalto and g.z == 0:
                    g.x += 15
                    break
        if keys[pygame.K_DOWN]:
            for g in self.team_1.players:
                if g.selected and g.y > Y_BORDO_2_CAMPO + 15 and not g.inSalto and g.z == 0:
                    g.y -= 15
                    break
        if keys[pygame.K_UP]:
            for g in self.team_1.players:
                if g.selected and g.y < Y_BORDO_2_CAMPO + Y_CAMPO - 15 and not g.inSalto and g.z == 0:
                    g.y += 15
                    if self.team_1.attackTo == 'left' and g.x > WIDTH - self.__calcoloCateto(g.y) - 140:
                        g.x = WIDTH - self.__calcoloCateto(g.y) - 140
                    elif g.x < self.__calcoloCateto(g.y) - 20:
                        g.x = self.__calcoloCateto(g.y) - 20
                    break
        if not keys[pygame.K_p] and self.team_1.isInSceltaTiro:
            self.ball.staPalleggiando = False
            self.ball.y += self.ball.z
            self.ball.z = 0
            self.ball.isInTiro = True
            for g in self.team_1.players:
                if g.selected:
                    g.haLaPalla = True
            self.ball.x0, self.ball.y0 = self.ball.x, HEIGHT - self.ball.y
            self.ball.preparazioneTiro()
            self.ball.calcTraiettoria(self.ball.x0)
            self.team_1.isInSceltaTiro = False

    def checkAzioniTeam_2(self, key):
        if key == pygame.K_SPACE:
            self.ball.staPalleggiando = False
            for p in self.team_1.players:
                if p.selected:
                    p.inSalto = True
            if self.team_1.attackTo == 'left':
                self.ball.x += SIZE_BALL[0] / 2
            else:
                self.ball.x -= SIZE_BALL[0] / 2
        elif key == pygame.K_l:
            iNewSelected, distance = -1, (WIDTH ** 2 + HEIGHT ** 2) ** (1 / 2)
            for i, g in enumerate(self.team_1.players):
                if g.selected:
                    g.selected = False
                    continue
                _distance = (abs(g.x - self.ball.x) ** 2 + abs(g.y - self.ball.y) ** 2) ** 0.5
                if iNewSelected == -1 or _distance < distance:
                    distance = _distance
                    iNewSelected = i
            if iNewSelected != -1:
                self.team_1.players[iNewSelected].selected = True
        elif key == pygame.K_p and not self.ball.isInTiro:
            self.team_1.isInSceltaTiro = True
            self.team_1.dirFrecciaTiro = HEIGHT - self.team_1.imgFrecciaTiro.get_height()

    def __calcoloCateto(self, y):
        i = y / math.cos(15)
        return (i ** 2 - y ** 2) ** .5


class Ball:
    def __init__(self):
        self.imgBall = pygame.image.load('images/palla.png')
        self.x = WIDTH / 2 - SIZE_BALL[0] / 2
        self.y = Y_CAMPO / 2 + Y_BORDO_2_CAMPO + SIZE_BALL[1] + 120
        self.z = 0
        self.staPalleggiando = False
        self.isPalleggioVersoAlto = True
        self.x0 = self.x
        self.y0 = self.y
        self.a_b_c = {'a': 0, 'b': 0, 'c': 0}
        self.isInTiro = False

    def movPalla(self):
        if self.isInTiro:
            if self.x >= COORD_CANESTRO_2['x']:
                self.isInTiro = False
            elif self.x + 12 < COORD_CANESTRO_2['x']:
                self.calcTraiettoria(self.x + 12)
            else:
                self.x = COORD_CANESTRO_2['x']
                self.calcTraiettoria(self.x)
        else:
            self.palleggia()

    def palleggia(self):
        if self.staPalleggiando and self.isPalleggioVersoAlto and self.z < 20:
            self.z += 7
            if self.z >= 20:
                self.isPalleggioVersoAlto = False
        elif self.staPalleggiando and not self.isPalleggioVersoAlto and self.z > 0:
            self.z -= 7
            if self.z <= 0:
                self.isPalleggioVersoAlto = True

    def coordToDraw(self):
        return self.x, HEIGHT - self.y - self.z

    def preparazioneTiro(self):
        x0, x1 = self.x0, COORD_CANESTRO_2['x'] - SIZE_BALL[0] / 2 - 5
        y0, y1 = self.y0, HEIGHT - COORD_CANESTRO_2['y'] - COORD_CANESTRO_2['z'] + SIZE_BALL[1] / 4
        x2, y2 = x0 + 3 * (x1 - x0) / 4, HEIGHT - 45
        print(x2, y2)

        a = np.array([[x0 ** 2, x0, 1], [x1 ** 2, x1, 1], [x2 ** 2, x2, 1]])
        b = np.array([y0, y1, y2])
        sol = np.linalg.solve(a, b)
        self.a_b_c['a'] = sol[0]
        self.a_b_c['b'] = sol[1]
        self.a_b_c['c'] = sol[2]

    def calcTraiettoria(self, x):
        y = self.a_b_c['a'] * x * x + self.a_b_c['b'] * x + self.a_b_c['c']
        self.x = x
        self.y = y


class Team:
    def __init__(self, n):
        self.attackTo = 'right' if n == 1 else 'left'
        self.imgTriangle = pygame.image.load('images/triangolo_bianco.png') if n == 1 else pygame.image.load('images/triangolo_verde.png')
        self.imgBarraTiro = pygame.image.load('images/barraTiro.png')
        self.imgFrecciaTiro = pygame.image.load('images/freccia_verde.png')
        self.players = [Player('images/players/faces/kobe_bryant.png', False, n, 800, True, True)]  # ,
        # Player('images/players/faces/domantas_sabonis.png', True, n, 650),
        # Player('images/players/faces/kevin_durant.png', False, n, 500)]
        self.isInSceltaTiro = False
        self.dirFrecciaTiro = 'up'
        self.yFrecciaTiro = HEIGHT - self.imgFrecciaTiro.get_height()

    def writeBarraTiro(self, ball: Ball, display):
        if self.isInSceltaTiro or ball.isInTiro:
            hGeneric = HEIGHT - self.imgFrecciaTiro.get_height() / 2
            if self.attackTo == 'right':
                display.blit(self.imgBarraTiro, (10, hGeneric - self.imgBarraTiro.get_height()))
            if hGeneric - self.yFrecciaTiro <= 147 or hGeneric - self.yFrecciaTiro >= 262:
                _img = pygame.image.load('images/freccia_grigia.png')
            elif 148 <= hGeneric - self.yFrecciaTiro <= 173 or 236 <= hGeneric - self.yFrecciaTiro <= 261:
                _img = pygame.image.load('images/freccia_arancione.png')
            elif 174 <= hGeneric - self.yFrecciaTiro <= 185 or 224 <= hGeneric - self.yFrecciaTiro <= 235:
                _img = pygame.image.load('images/freccia_gialla.png')
            else:
                _img = pygame.image.load('images/freccia_verde.png')

            if self.attackTo == 'right':
                display.blit(_img, (10 + self.imgBarraTiro.get_width(), self.yFrecciaTiro))

            if self.dirFrecciaTiro == 'up' and self.isInSceltaTiro:
                if self.yFrecciaTiro - 20 <= HEIGHT - self.imgFrecciaTiro.get_height() / 2 - self.imgBarraTiro.get_height():
                    self.yFrecciaTiro = HEIGHT - self.imgFrecciaTiro.get_height() / 2 - self.imgBarraTiro.get_height()
                    self.dirFrecciaTiro = 'down'
                else:
                    self.yFrecciaTiro -= 20
            elif self.isInSceltaTiro:
                if self.yFrecciaTiro + 20 >= HEIGHT - self.imgFrecciaTiro.get_height():
                    self.yFrecciaTiro = HEIGHT - self.imgFrecciaTiro.get_height()
                    self.dirFrecciaTiro = 'up'
                else:
                    self.yFrecciaTiro += 20


class Player:
    def __init__(self, path, isWhite, team, x, selected=False, haLaPalla=False):
        self.imgFace2Right = pygame.image.load(path)
        self.imgFace2Left = pygame.transform.flip(self.imgFace2Right, True, False)
        self.imgShoes2Right = pygame.image.load('images/players/shoes.png')
        self.imgShoes2Left = pygame.transform.flip(self.imgShoes2Right, True, False)
        self.imgHand2Right = pygame.image.load('images/players/mano_bianca.png') if isWhite else pygame.image.load('images/players/mano_nera.png')
        self.imgHand2Left = pygame.transform.flip(self.imgHand2Right, True, False)
        self.imgTshirt2Right = pygame.image.load('images/players/maglia_1.png') if team == 1 else pygame.image.load('images/players/maglia_2.png')
        self.imgTshirt2Left = pygame.transform.flip(self.imgTshirt2Right, True, False)
        self.x = x  # temporaneo
        self.y = Y_CAMPO / 2 + Y_BORDO_2_CAMPO  # + self.imgTshirt2Right.get_height() + self.imgFace2Right.get_height()
        self.z = 0
        self.isWhite = isWhite
        self.selected = selected
        self.inSalto = False
        self.haLaPalla = haLaPalla

    def updatePlayer(self, ball: Ball, verso):
        if self.selected:
            if self.inSalto and self.z < 120:
                self.z += 9
                if not ball.isInTiro:
                    ball.z += 9
                return
            elif self.inSalto and 120 < self.z < 135:
                self.z += 4.5
                if not ball.isInTiro:
                    ball.z += 4.5
                return

            self.inSalto = False
            if not ball.isInTiro:
                ball.staPalleggiando = True
                self.haLaPalla = True

            if self.z > 0:
                self.z -= 9
                if not ball.isInTiro:
                    ball.z -= 9
            elif self.z < 0:
                self.z = 0
                if not ball.isInTiro:
                    ball.z = 0

            if not ball.isInTiro:
                if verso == 'left':
                    ball.x = self.x + 30
                    ball.y = self.y + self.imgShoes2Left.get_height() + self.imgHand2Left.get_height() - SIZE_BALL[1] / 2
                else:
                    ball.x = self.x + self.imgFace2Left.get_width() + self.imgHand2Left.get_width() - 30
                    ball.y = self.y + self.imgShoes2Right.get_height() + self.imgHand2Right.get_height() - SIZE_BALL[1] / 2

    def drawPlayer(self, display, verso, triangolo):
        img1 = self.imgFace2Right if verso == 'right' else self.imgFace2Left
        img2 = self.imgTshirt2Right if verso == 'right' else self.imgTshirt2Left
        img3 = self.imgShoes2Right if verso == 'right' else self.imgShoes2Left
        img4 = self.imgHand2Right if verso == 'right' else self.imgHand2Left

        if verso == 'right':
            display.blit(img2, (self.x + (img1.get_width() - img2.get_width()) / 2 + 5, HEIGHT - self.y - img3.get_height() - img2.get_height() + 10 - self.z))
            display.blit(img1, (self.x, HEIGHT - self.y - img3.get_height() - img2.get_height() - img1.get_height() + 26 - self.z))
            if self.selected:
                display.blit(triangolo, (self.x + (img1.get_width() - triangolo.get_width()) / 2, HEIGHT - self.y - img3.get_height() - img2.get_height() - img1.get_height() - 20 - self.z))
            if self.inSalto:
                newShoes = pygame.image.load('images/players/shoesInSalto.png') if verso == 'right' else pygame.transform.flip(pygame.image.load('images/players/shoesInSalto.png'), True, False)
                display.blit(newShoes, (self.x + (img1.get_width() - img2.get_width()) / 2, HEIGHT - self.y - img3.get_height() - self.z - 5))
                newHand = pygame.image.load('images/players/mano_bianca_inSalto.png') if self.isWhite else pygame.image.load('images/players/mano_nera_inSalto.png')
                display.blit(newHand, (self.x + img1.get_width() - img4.get_width() / 1.5, HEIGHT - self.y - img3.get_height() - newHand.get_height() - self.z))
            else:
                display.blit(img3, (self.x + (img1.get_width() - img2.get_width()) / 2, HEIGHT - self.y - img3.get_height() - self.z))
                display.blit(img4, (self.x + img1.get_width() - img4.get_width() / 1.5 + 15, HEIGHT - self.y - img3.get_height() - img4.get_height() - self.z - 20))
        else:
            display.blit(img2, (self.x + img1.get_width() + (img1.get_width() - img2.get_width()) / 2 - 5, HEIGHT - self.y - img3.get_height() - img2.get_height() + 10 - self.z))
            display.blit(img1, (self.x + img1.get_width(), HEIGHT - self.y - img3.get_height() - img2.get_height() - img1.get_height() + 26 - self.z))
            if self.selected:
                display.blit(triangolo, (self.x + img1.get_width() + (img1.get_width() - triangolo.get_width()) / 2, HEIGHT - self.y - img3.get_height() - img2.get_height() - img1.get_height() - 20 - self.z))
            if self.inSalto:
                newShoes = pygame.image.load( 'images/players/shoesInSalto.png') if verso == 'right' else pygame.transform.flip(pygame.image.load('images/players/shoesInSalto.png'), True, False)
                display.blit(newShoes, (self.x + img1.get_width(), HEIGHT - self.y - img3.get_height() - self.z - 5))
                newHand = pygame.transform.flip(pygame.image.load('images/players/mano_bianca_inSalto.png') if self.isWhite else pygame.image.load('images/players/mano_nera_inSalto.png'), True, False)
                display.blit(newHand, (self.x + img1.get_width() - img4.get_width() / 4, HEIGHT - self.y - img3.get_height() - newHand.get_height() - self.z))
            else:
                display.blit(img3, (self.x + img1.get_width(), HEIGHT - self.y - img3.get_height() - self.z))
                display.blit(img4, (self.x + img1.get_width() - img4.get_width() / 4 - 15, HEIGHT - self.y - img3.get_height() - img4.get_height() - self.z - 20))


def main():
    pygame.init()
    game = Game()

    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                game.checkAzioniTeam_2(e.key)

        game.checkMovimentiTeam_2()
        pygame.time.Clock().tick(FPS)
        game.reloadWindow()
        pygame.display.update()


if __name__ == '__main__':
    main()
