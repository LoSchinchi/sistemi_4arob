import math
import os
import pygame
import numpy as np
import sys
from pygame.locals import *
from random import randint
from time import time as Time


WIDTH = 1577
HEIGHT = 682
TITLE = 'Basketball 3 v 3'
FPS = 60

EFF_MIN_PER_GAME = 48
MIN_PER_GAME = 12
EFF_MIN_PER_QUARTER = 12
MIN_PER_QUARTER = MIN_PER_GAME / 4

SIZE_BALL = (40, 40)
COORD_CANESTRO_2 = (WIDTH - 250 - SIZE_BALL[0], 95)  # y: 202, z: HEIGHT - 307
FERRO_1_CANESTRO_2 = (COORD_CANESTRO_2[0] - 25, COORD_CANESTRO_2[1])
FERRO_2_CANESTRO_2 = (COORD_CANESTRO_2[0] + 25, COORD_CANESTRO_2[1])
COORD_CANESTRO_1 = (250 + SIZE_BALL[0], 95 - SIZE_BALL[1])  # y: 202, z: HEIGHT - 307
FERRO_1_CANESTRO_1 = (COORD_CANESTRO_1[0] + 25, COORD_CANESTRO_1[1])
FERRO_2_CANESTRO_1 = FERRO_1_CANESTRO_1  # non (COORD_CANESTRO_1[0] - 25, COORD_CANESTRO_1[1]) per tempo
Y_TRAIETTORIA_TIRO = 45
Y_RIM_FERRO = 75 + SIZE_BALL[1]
Y_CANESTRI = HEIGHT - 202

X_CAMPO = 1433
Y_CAMPO = 245
Y_BORDO_2_CAMPO = 47
LINEA_3_CAN_2 = ({'x': 1025, 'y': 299.5}, {'x': 1205, 'y': 274.5}, {'x': 1010, 'y': 259.5}, {'x': 980, 'y': 244.5},
                 {'x': 965, 'y': 229.5}, {'x': 965, 'y': 214.5}, {'x': 965, 'y': 199.5}, {'x': 965, 'y': 184.5},
                 {'x': 980, 'y': 169.5}, {'x': 995, 'y': 154.5}, {'x': 1010, 'y': 139.5}, {'x': 1025, 'y': 124.5},
                 {'x': 1055, 'y': 109.5}, {'x': 1085, 'y': 94.5}, {'x': WIDTH, 'y': 79.5}, {'x': WIDTH, 'y': 64.5},
                 {'x': WIDTH, 'y': 49.5})  # 'x' da sx a dx, facendo -60 si trovano con verso sx
LINEA_3_CAN_1 = ({'x': 0, 'y': 299.5}, {'x': 0, 'y': 274.5}, {'x': 267, 'y': 259.5}, {'x': 327, 'y': 244.5},
                 {'x': 357, 'y': 229.5}, {'x': 387, 'y': 214.5}, {'x': 402, 'y': 199.5}, {'x': 417, 'y': 184.5},
                 {'x': 432, 'y': 169.5}, {'x': 417, 'y': 154.5}, {'x': 402, 'y': 139.5}, {'x': 387, 'y': 124.5},
                 {'x': 357, 'y': 109.5}, {'x': 327, 'y': 94.5}, {'x': 0, 'y': 79.5}, {'x': 0, 'y': 64.5},
                 {'x': 0, 'y': 49.5})  # 'x' da sx a dx, facendo +60 si trovano con verso sx
DEF_BARRA_TIRO = {'i': 230, 'v': 12}


class FirstWindow:
    def __init__(self):
        self.imgSfondo = pygame.image.load('images/campoSchermataIniz.png')
        self.display = pygame.display.set_mode(self.imgSfondo.get_size())
        self.inSchermataIniz = True
        pygame.display.set_caption(TITLE)

        self.fonts = {'input': pygame.font.Font(None, 40), 'names': pygame.font.Font(None, 30)}
        self.colors = {'active': pygame.Color('gold'), 'inactive': pygame.Color('white'), 'names': pygame.Color('black')}
        self.inpName_1 = {'box': pygame.Rect(300, 100, 140, 40), 'color': self.colors['inactive'], 'active': False, 'text': 'nome team 1'}
        self.inpName_2 = {'box': pygame.Rect(WIDTH - 300, 100, 140, 40), 'color': self.colors['inactive'], 'active': False, 'text': 'nome team 2'}

        self.listPlayers = []
        self.indGiocUsciti = []
        self.paths = os.listdir('images/players/faces')
        while len(self.listPlayers) < 6:
            n = randint(0, len(self.paths) - 1)
            if n in self.indGiocUsciti:
                continue

            self.indGiocUsciti.append(n)
            self.listPlayers.append({'path': self.paths[n],
                                     'freccia su': pygame.image.load('images/frecciaSceltaGiocSu.png'),
                                     'freccia giu': pygame.image.load('images/frecciaSceltaGiocGiu.png'),
                                     'name': self.fonts['names'].render(self.paths[n][:self.paths[n].index('_')].capitalize(), True, self.colors['names']),
                                     'surname': self.fonts['names'].render(self.paths[n][self.paths[n].index('_') + 1: -4].capitalize(), True, self.colors['names']),
                                     'index': n})

    def __printPlayer(self, i, g):
        imgTesta = pygame.image.load('images/players/faces/' + g['path'])
        imgCorpo = pygame.image.load('images/players/maglia_1.png') if i < 3 else pygame.image.load('images/players/maglia_2.png')
        imgScarpe = pygame.image.load('images/players/shoes.png')
        x = 200 + i * (imgTesta.get_width() + 100) if i < 3 else WIDTH - 200 - (2 - i % 3) * (imgTesta.get_width() + 100)

        self.display.blit(imgScarpe, (x + 20, 460))
        self.display.blit(imgCorpo, (x + 20, 450 - imgScarpe.get_height()))
        self.display.blit(imgTesta, (x, 460 - imgScarpe.get_height() - imgTesta.get_height()))
        self.display.blit(g['freccia su'], (x + imgTesta.get_width() / 2 - g['freccia su'].get_width() / 2, 320 - imgScarpe.get_height() - g['freccia su'].get_height()))
        self.display.blit(g['freccia giu'], (x + imgTesta.get_width() / 2 - g['freccia giu'].get_width() / 2, 570))
        self.display.blit(g['name'], (x + imgTesta.get_width() / 2 - g['name'].get_width() / 2, 510))
        self.display.blit(g['surname'], (x + imgTesta.get_width() / 2 - g['surname'].get_width() / 2, 540))

    def __indexEff(self, n):
        if n < -len(self.paths):
            return self.__indexEff(n + len(self.paths))
        elif n < 0:
            return len(self.paths) + n
        elif n >= len(self.paths):
            return self.__indexEff(n - len(self.paths))
        return n

    def __cambioGioc(self, n, g, i):
        g['index'], g['path'], self.indGiocUsciti[i] = n, self.paths[n], n
        g['name'] = self.fonts['names'].render(g['path'][:g['path'].index('_')].capitalize(), True, self.colors['names'])
        g['surname'] = self.fonts['names'].render(g['path'][g['path'].index('_') + 1: -4].capitalize(), True, self.colors['names'])

    def checkEvt(self, e):
        if e.type == MOUSEBUTTONDOWN:
            if self.inpName_1['box'].collidepoint(e.pos):
                self.inpName_1['active'] = not self.inpName_1['active']
                self.inpName_2['active'] = False
            elif self.inpName_2['box'].collidepoint(e.pos):
                self.inpName_2['active'] = not self.inpName_2['active']
                self.inpName_1['active'] = False
            else:
                self.inpName_1['active'] = False
                self.inpName_2['active'] = False

            self.inpName_1['color'] = self.colors['active'] if self.inpName_1['active'] else self.colors['inactive']
            self.inpName_2['color'] = self.colors['active'] if self.inpName_2['active'] else self.colors['inactive']

            for i, g in enumerate(self.listPlayers):
                pos = pygame.mouse.get_pos()
                head = pygame.image.load('images/players/faces/' + g['path'])
                x = 200 + i * (head.get_width() + 100) if i < 3 else WIDTH - 200 - (2 - i % 3) * (head.get_width() + 100)
                x += head.get_width() / 2 - g['freccia su'].get_width() / 2
                y = 320 - pygame.image.load('images/players/shoes.png').get_height() - g['freccia su'].get_height()

                if x <= pos[0] <= x + g['freccia su'].get_width() and y <= pos[1] <= y + g['freccia su'].get_height():
                    while self.__indexEff(g['index']) in self.indGiocUsciti:
                        g['index'] -= 1
                    self.__cambioGioc(self.__indexEff(g['index']), g, i)
                    break
                # non serve ri-assegnare la x perché le dim delle frecce sono uguali
                elif x <= pos[0] <= x + g['freccia giu'].get_width() and 570 <= pos[1] <= 570 + g['freccia giu'].get_height():
                    while self.__indexEff(g['index']) in self.indGiocUsciti:
                        g['index'] += 1
                    self.__cambioGioc(self.__indexEff(g['index']), g, i)
                    break

        if e.type == KEYDOWN and self.inpName_1['active']:
            if e.key == K_BACKSPACE:
                self.inpName_1['text'] = self.inpName_1['text'][:-1]
            else:
                self.inpName_1['text'] += e.unicode
        elif e.type == KEYDOWN and self.inpName_2['active']:
            if e.key == K_BACKSPACE:
                self.inpName_2['text'] = self.inpName_2['text'][:-1]
            else:
                self.inpName_2['text'] += e.unicode
        elif e.type == KEYDOWN and e.key == K_RETURN:
            self.inSchermataIniz = False

    def updateWindow(self):
        self.display.blit(self.imgSfondo, (0, 0))
        txt_sur_1 = self.fonts['input'].render(self.inpName_1['text'], True, self.inpName_1['color'])
        txt_sur_2 = self.fonts['input'].render(self.inpName_2['text'], True, self.inpName_2['color'])
        self.inpName_2['box'] = pygame.Rect(WIDTH - 300 - txt_sur_2.get_width(), 100, 140, 40)
        self.inpName_1['box'].w = max(200, txt_sur_1.get_width() + 10)
        self.inpName_2['box'].w = max(200, txt_sur_2.get_width() + 10)
        self.display.blit(txt_sur_1, (self.inpName_1['box'].x + 5, self.inpName_1['box'].y + 5))
        self.display.blit(txt_sur_2, (self.inpName_2['box'].x + 5, self.inpName_2['box'].y + 5))

        if self.inpName_1['text'].strip() == '' and not self.inpName_1['active']:
            self.inpName_1['text'] = 'nome team 1'
        if self.inpName_2['text'].strip() == '' and not self.inpName_2['active']:
            self.inpName_2['text'] = 'nome team 2'
        for i, g in enumerate(self.listPlayers):
            self.__printPlayer(i, g)

        txt_istruz = pygame.font.Font(None, 30).render('premere INVIO per continuare', True, 'white')
        self.display.blit(txt_istruz, (WIDTH / 2 - txt_istruz.get_width() / 2, HEIGHT - 30))


class SecondWindow:
    def __init__(self, display, name1, name2):
        self.imgSfondo = pygame.image.load('images/campoSchermataIniz.png')
        self.name1 = name1
        self.name2 = name2
        self.display = display
        self.inSchermataRegole = True
        self.fontNomi = pygame.font.Font(None, 46)
        self.scopoTasti = pygame.font.Font(None, 30)
        self.commandsRight = {'su': 'freccia su', 'giu': 'freccia giu', 'destra': 'freccia destra', 'sinistra': 'freccia sinistra',
                              'salto': 'spazio', 'tiro': 'P', 'passaggio': 'O', 'cambio giocatore': 'L'}
        self.commandsLeft = {'su': 'W', 'giu': 'S', 'destra': 'D', 'sinistra': 'A',
                             'salto': 'E', 'tiro': 'X', 'passaggio': 'C', 'cambio giocatore': 'R'}

    def updateWindow(self):
        self.display.blit(self.imgSfondo, (0, 0))
        self.__visCommand(200, False)
        self.__visCommand(900)
        txt_istruz = pygame.font.Font(None, 30).render('premere INVIO per iniziare', True, 'white')
        self.display.blit(txt_istruz, (WIDTH / 2 - txt_istruz.get_width() / 2, HEIGHT - 30))

    def __visCommand(self, x, isRight=True):
        col = pygame.Color('lightblue') if isRight else pygame.Color('orange')
        diz = self.commandsRight if isRight else self.commandsLeft
        startY = 200

        for k, v in diz.items():
            txt = self.fontNomi.render(k + ' -> ' + v, True, col)
            self.display.blit(txt, (x, startY))
            startY += 35

    def checkEvt(self, e):
        if e.type == KEYDOWN and e.key == K_RETURN:
            self.inSchermataRegole = False


class Game:
    def __init__(self, display, name1, name2, listPl):
        self.display = display
        self.imgCampo = pygame.image.load('images/campo.png')
        self.display.blit(self.imgCampo, (0, 0))
        self.ball = Ball()
        self.team_1 = Team(1, name1, listPl[:3])
        self.team_2 = Team(2, name2, listPl[3:])
        self.results = {'font': pygame.font.Font(None, 35), 'color': pygame.Color('white')}
        self.atStart = {'start azione': False, 'is start game': True, 'team starter': self.team_1, 'lancio palla': True, 'palla presa': False}
        self.quartoInGame = 0
        self.timers = {'tQuarto': None, 't24sec': None, 'tMovs': None, 'secQuarto': 720, 'sec24sec': 24, 'secMovs': 7, 'stopped': False, 'tMusic': Time()}
        self.txtTimer = {'font qrt': pygame.font.Font(None, 35), 'col qrt': pygame.Color('orange'), 'font 24sec': pygame.font.Font(None, 28), 'col 24sec': pygame.Color('white')}
        self.suoniPubblico = pygame.mixer.Sound('sounds/vociPubblico.mp3')

        self.suoniPubblico.play()

    def reloadWindow(self):
        if self.timers['tMusic'] + self.suoniPubblico.get_length() <= Time():
            self.suoniPubblico.play()
            self.timers['tMusic'] = Time()

        if self.timers['tQuarto'] is None and not self.atStart['is start game'] and self.ball.z == 0:
            self.timers['tQuarto'] = Time()
        if self.timers['t24sec'] is None and not self.atStart['is start game'] and self.ball.z == 0:
            self.timers['t24sec'] = Time()
        if self.timers['tMovs'] is None and not self.atStart['is start game']:
            self.timers['tMovs'] = Time()

        if self.timers['secQuarto'] <= 0 or self.timers['sec24sec'] <= 0:
            pygame.mixer.Sound('sounds/sirena.wav').play()
        if self.timers['secQuarto'] <= 0:
            self.startNewQuarter()
            return

        self.display.blit(self.imgCampo, (0, 0))
        if self.timers['tQuarto'] is not None and not self.timers['stopped']:
            self.__printTimeQuarter()
            self.__printTimer24sec()
            txtRis_1 = self.results['font'].render(self.team_1.name + ' ' * 20 + str(self.team_1.puntiPartita), True, self.results['color'])
            txtRis_2 = self.results['font'].render(str(self.team_2.puntiPartita) + ' ' * 20 + self.team_2.name, True, self.results['color'])
            self.display.blit(txtRis_1, (300, 55))
            self.display.blit(txtRis_2, (WIDTH - 300 - txtRis_2.get_width(), 55))

        if self.atStart['is start game']:
            self.startGame()
            self.__updateAndShowPlayers()
            self.display.blit(self.ball.imgBall, (self.ball.x, HEIGHT - self.ball.y - self.ball.z))
            return
        elif self.atStart['palla presa']:
            self.__updateAndShowPlayers()
            self.display.blit(self.ball.imgBall, (self.ball.x, HEIGHT - self.ball.y - self.ball.z))
            if not self.ball.isAlone:
                self.atStart['team starter'] = self.team_1 if self.team_1.isInPossesso() else self.team_2
                self.atStart['palla presa'] = False
                self.startNewQuarter()
            return

        self.team_1.writeBarraTiro(self.ball, self.display)
        self.team_2.writeBarraTiro(self.ball, self.display)

        if not self.ball.onTiro['is can'] and not self.atStart['start azione']:
            self.timers['stopped'] = False

        if self.timers['stopped']:
            self.timers['sec24sec'] = 24
            self.timers['secMovs'] = 7

        if self.ball.onTiro['in tiro'] and self.ball.onTiro['team tir'] is not None:
            self.timers['sec24sec'] = 24
            self.timers['t24sec'] = Time()
            if self.ball.onTiro['team tir'] == self.team_1:
                self.team_1.setGiocCheHaTirato()
            else:
                self.team_2.setGiocCheHaTirato()
            self.ball.tiro()
        elif self.ball.onTiro['is rimb'] and not self.ball.onTiro['in tiro']:
            for g in self.team_1.players + self.team_2.players:
                g.haLaPalla = False

            if not self.ball.onTiro['sound fatto']:
                self.ball.onTiro['sound fatto'] = True
                pygame.mixer.Sound('sounds/ferroColpito.mp3').play()

            self.ball.rimbalzoFerro()
            self.team_1.yFrecciaTiro = HEIGHT - self.team_1.imgFrecciaTiro.get_height()
            self.team_2.yFrecciaTiro = HEIGHT - self.team_2.imgFrecciaTiro.get_height()
        elif self.ball.onTiro['is can'] and not self.ball.onTiro['in tiro']:
            self.timers['stopped'] = True
            if not self.ball.onTiro['sound fatto']:
                self.ball.onTiro['sound fatto'] = True
                pygame.mixer.Sound('sounds/esultanza.mp3').play()
                pygame.mixer.Sound('sounds/reteCanestro.mp3').play()
            self.ball.completeCanestro()
            self.team_1.yFrecciaTiro = HEIGHT - self.team_1.imgFrecciaTiro.get_height()
            self.team_2.yFrecciaTiro = HEIGHT - self.team_2.imgFrecciaTiro.get_height()
            if self.ball.onTiro['team tir'] == self.team_1 and not self.team_1.puntiGiaAgg:
                self.team_1.aggiornaPunteggio()
                self.team_1.puntiGiaAgg = True
                self.team_2.inizioNewAzioneOff(self.ball)
                self.team_1.inizioNewAzioneDif()
                self.timers['stopped'] = True
                return
            elif self.ball.onTiro['team tir'] == self.team_2 and not self.team_2.puntiGiaAgg:
                self.team_2.aggiornaPunteggio()
                self.team_2.puntiGiaAgg = True
                self.team_1.inizioNewAzioneOff(self.ball)
                self.team_2.inizioNewAzioneDif()
                self.timers['stopped'] = True
                return
        elif self.ball.onPassaggio['in pass']:
            self.ball.passaggio()
        else:
            self.ball.palleggia()

        self.display.blit(self.ball.imgBall, (self.ball.x, HEIGHT - self.ball.y - self.ball.z))
        self.__updateAndShowPlayers()
        self.__checkMov()

    def __printTimeQuarter(self):
        t = Time()
        if round(t, 2) - round(self.timers['tQuarto'], 2) >= MIN_PER_QUARTER / EFF_MIN_PER_QUARTER * (720 - self.timers['secQuarto'] + 1):
            self.timers['secQuarto'] -= 1
        sec = str(self.timers['secQuarto'] % 60) if self.timers['secQuarto'] % 60 >= 10 else '0' + str(self.timers['secQuarto'] % 60)
        minutes = str(self.timers['secQuarto'] // 60) if self.timers['secQuarto'] // 60 >= 10 else '0' + str(self.timers['secQuarto'] // 60)
        stringa = minutes + ' : ' + sec
        txt = self.txtTimer['font qrt'].render(stringa, True, self.txtTimer['col qrt'])
        self.display.blit(txt, (WIDTH / 2 - txt.get_width() / 2, 60))

    def __printTimer24sec(self):
        if self.timers['sec24sec'] == 0:
            self.timers['sec24sec'] = 24
            self.timers['t24sec'] = Time()
            return

        t = Time()
        if round(t, 2) - round(self.timers['t24sec'], 2) >= 24 - self.timers['sec24sec'] + 1:
            self.timers['sec24sec'] -= 1
        stringa = '00 : ' + (str(self.timers['sec24sec']) if self.timers['sec24sec'] >= 10 else '0' + str(self.timers['sec24sec']))
        txt = self.txtTimer['font 24sec'].render(stringa, True, self.txtTimer['col 24sec'])
        self.display.blit(txt, (WIDTH / 2 - txt.get_width() / 2, 110))

    def __checkMov(self):
        t = Time()
        if round(t, 2) - round(self.timers['tMovs']) >= 7 - self.timers['secMovs'] + 1:
            self.timers['secMovs'] -= 1

        if self.timers['secMovs'] == 0:
            team = self.team_1 if self.team_1.isInPossesso() else self.team_2
            if team.checkNMov == 0 and not self.timers['stopped']:
                team.creaMovimento()
                self.timers['tMovs'] = Time()
                self.timers['secMovs'] = 7

    def __updateAndShowPlayers(self):
        listTuttiGioc = self.team_1.players + self.team_2.players

        for i in range(1, len(listTuttiGioc)):
            for j in range(0, i):
                if listTuttiGioc[i].y > listTuttiGioc[j].y:
                    listTuttiGioc[i], listTuttiGioc[j] = listTuttiGioc[j], listTuttiGioc[i]

        for g in listTuttiGioc:
            team = self.team_1 if g in self.team_1.players else self.team_2
            g.updatePlayer(self.ball, team.attackTo, team, self.atStart['start azione'])
            if not g.selected:
                g.giratoDa = 'right' if g.x < self.ball.x else 'left'
            else:
                g.giratoDa = team.attackTo
            g.drawPlayer(self.display, team.imgTriangle)

    def startNewQuarter(self):
        self.timers['tQuarto'] = Time()
        self.timers['secQuarto'] = 720
        self.timers['t24sec'] = Time()
        self.timers['sec24sec'] = 24
        self.timers['tMovs'] = Time()
        self.timers['secMovs'] = 7
        self.quartoInGame += 1
        otherTeam = self.team_2 if self.atStart['team starter'] == self.team_1 else self.team_1

        if self.quartoInGame == 1:
            for g in self.atStart['team starter'].players:
                if not g.haLaPalla:
                    g.setObj_x_off(self.atStart['team starter'])
            for g in otherTeam.players:
                if not g.selected:
                    g.setObj_x_dif(otherTeam)
        elif self.quartoInGame == 4:
            self.atStart['team starter'].inizioNewAzioneOff(self.ball)
            otherTeam.inizioNewAzioneDif()
        else:
            otherTeam.inizioNewAzioneOff(self.ball)
            self.atStart['team starter'].inizioNewAzioneDif()
        self.atStart['start azione'] = True

    def startGame(self):
        if self.ball.z > 300:
            self.atStart['lancio palla'] = False
        if self.atStart['lancio palla']:
            self.ball.z += 30
            return
        else:
            self.ball.z -= 30
        if self.ball.z == 0:
            self.atStart['is start game'] = False
            self.atStart['palla presa'] = True

    def startCronometri(self):
        pass

    def __checkMovimentiComune(self, team, K_up, K_down, K_right, K_left, K_tiro):
        keys = pygame.key.get_pressed()
        if keys[K_left] and not team.atStartAzione:
            team.attackTo = 'left'
            for g in team.players:
                if g.selected and g.x > self.__calcoloCateto(g.y) - 30 and not g.inSalto and g.z == 0:
                    g.x -= 15
                    g.giaMossa = True
                    break
        if keys[K_right] and not team.atStartAzione:
            team.attackTo = 'right'
            for g in team.players:
                if g.selected and g.x < WIDTH - self.__calcoloCateto(g.y) - 140 and not g.inSalto and g.z == 0:
                    g.x += 15
                    g.giaMossa = True
                    break
        if keys[K_down] and not team.atStartAzione:
            for g in team.players:
                if g.selected and g.y > Y_BORDO_2_CAMPO + 15 and not g.inSalto and g.z == 0:
                    g.y -= 15
                    g.giaMossa = True
                    break
        if keys[K_up] and not team.atStartAzione:
            for g in team.players:
                if g.selected and g.y < Y_BORDO_2_CAMPO + Y_CAMPO - 15 and not g.inSalto and g.z == 0:
                    g.y += 15
                    g.giaMossa = True
                    if team.attackTo == 'left' and g.x > WIDTH - self.__calcoloCateto(g.y) - 140:
                        g.x = WIDTH - self.__calcoloCateto(g.y) - 140
                    elif g.x < self.__calcoloCateto(g.y) - 20:
                        g.x = self.__calcoloCateto(g.y) - 20
                    break
        if not keys[K_tiro] and team.isInSceltaTiro:
            if self.ball.onTiro['sound fatto']:
                self.ball.onTiro['sound fatto'] = False
            self.ball.onPalleggio['in pall'] = False
            self.ball.y += self.ball.z
            self.ball.z = 0
            self.ball.onTiro['in tiro'] = True
            for g in team.players:
                if g.selected:
                    g.giaMossa = False
                    g.haLaPalla = False
                    self.ball.yGiocCheTira = g.y
                    self.ball.gCheHaTirato = g
            self.ball.x0, self.ball.y0 = self.ball.x, HEIGHT - self.ball.y

            self.ball.preparazioneTiro(HEIGHT - team.imgFrecciaTiro.get_height() / 2 - team.yFrecciaTiro)
            self.ball.calcTraiettoria(self.ball.x0)
            for g in team.players:
                if g.selected:
                    g.haLaPalla = False
            self.ball.isAlone = True
            team.isInSceltaTiro = False
            team.dirFrecciaTiro = 'up'

    def checkMovimentiTeam_1(self):
        self.__checkMovimentiComune(self.team_1, K_w, K_s, K_d, K_a, K_x)

    def checkMovimentiTeam_2(self):
        self.__checkMovimentiComune(self.team_2, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_p)

    def __checkAzioniComune(self, key, team, K_salto, K_cambioG, K_tiro, K_passaggio):
        if key == K_salto and not self.atStart['start azione']:
            self.ball.onPalleggio['in pall'] = False
            for p in team.players:
                if p.selected:
                    p.inSalto = True
            if team.attackTo == 'left':
                self.ball.x += SIZE_BALL[0] / 2
            else:
                self.ball.x -= SIZE_BALL[0] / 2
        elif key == K_cambioG:
            self.atStart['start azione'] = False
            iNewSelected, distance = -1, (WIDTH ** 2 + HEIGHT ** 2) ** (1 / 2)
            for i, g in enumerate(team.players):
                if g.selected and g.haLaPalla:
                    return
                if g.selected:
                    g.selected = False
                    continue
                _distance = (abs(g.x - self.ball.x) ** 2 + abs(g.y - self.ball.y) ** 2) ** 0.5
                if iNewSelected == -1 or _distance < distance:
                    distance = _distance
                    iNewSelected = i
            if iNewSelected != -1:
                team.players[iNewSelected].selected = True
        elif key == K_tiro and not self.ball.onTiro['in tiro']:
            self.atStart['start azione'] = False
            self.ball.onTiro['team tir'] = team

            for g in team.players:
                if g.haLaPalla:
                    team.isInSceltaTiro = True
                    team.puntiGiaAgg = False
                    team.setVelBarraTiro(g.x, g.y)
                    g.haLaPalla = False
            self.ball.setVelInTiro(team.velBarraTiro)
        elif key == K_passaggio and team.isInPossesso():
            self.atStart['start azione'] = True
            self.timers['stopped'] = False
            team.atStartAzione = False
            gSel = None
            arrAltriGioc = [g for g in team.players if not g.selected]
            for g in team.players:
                if g.selected:
                    gSel = g
                    g.giaMossa = False

            gRicev, dist = None, -1
            for g in arrAltriGioc:
                if g.inMovimento:
                    gRicev = g
            if gRicev is None:
                for g in arrAltriGioc:
                    __dist = (abs(gSel.x - g.x) ** 2 + abs(gSel.y + gSel.z - g.y) ** 2) ** .5
                    if __dist < dist or dist == -1:
                        dist = __dist
                        gRicev = g

            self.ball.onPassaggio['in pass'] = True
            self.ball.onPalleggio['in pall'] = False
            gSel.haLaPalla = False
            self.ball.preparazionePassaggio(gSel, gRicev)

    def checkAzioniTeam_1(self, key):
        self.__checkAzioniComune(key, self.team_1, K_e, K_r, K_x, K_c)

    def checkAzioniTeam_2(self, key):
        self.__checkAzioniComune(key, self.team_2, K_SPACE, K_l, K_p, K_o)

    def __calcoloCateto(self, y):
        i = y / math.cos(15)
        return (i ** 2 - y ** 2) ** .5


class Ball:
    def __init__(self):
        self.imgBall = pygame.image.load('images/palla.png')
        self.isAlone = True
        self.x = WIDTH / 2 - SIZE_BALL[0] / 2
        self.y = Y_CAMPO / 2 + Y_BORDO_2_CAMPO + SIZE_BALL[1]
        self.z = 0
        self.x0 = self.x
        self.y0 = self.y
        self.yGiocCheTira = -1
        self.a_b_c = {'a': 0, 'b': 0, 'c': 0}
        self.m_q = {'m': 0, 'q': 0}
        self.listX = []
        self.onPalleggio = {'in pall': False, 'verso alto': True}
        self.onPassaggio = {'gRicev': None, 'gPass': None, 'in pass': False}
        self.onTiro = {'team tir': None, 'in tiro': False, 'is rimb': False, 'is can': False, 'calc rimb fatto': False, 'vel': 12, 'sound fatto': False}

    def setVelInTiro(self, vBarra):
        self.onTiro['vel'] = vBarra / 2

    def palleggia(self):
        if self.onPalleggio['in pall'] and self.onPalleggio['verso alto'] and self.z < 20:
            self.z += 7
            if self.z >= 20:
                self.onPalleggio['verso alto'] = False
        elif self.onPalleggio['in pall'] and not self.onPalleggio['verso alto'] and self.z > 0:
            self.z -= 7
            if self.z <= 0:
                self.onPalleggio['verso alto'] = True

    def preparazioneTiro(self, yBarraTiro):
        if yBarraTiro <= 185:
            coo = FERRO_1_CANESTRO_2 if self.onTiro['team tir'].nTeam == 1 else FERRO_1_CANESTRO_1
        elif yBarraTiro >= 224:
            coo = FERRO_2_CANESTRO_2 if self.onTiro['team tir'].nTeam == 1 else FERRO_2_CANESTRO_1
        else:
            coo = COORD_CANESTRO_2 if self.onTiro['team tir'].nTeam == 1 else COORD_CANESTRO_1

        x0, x1 = self.x0, coo[0] - SIZE_BALL[0] / 2 - 5
        y0, y1 = HEIGHT - self.y0, HEIGHT - coo[1] if x1 > x0 else HEIGHT - coo[1] - SIZE_BALL[1] * 3 / 2
        x2, y2 = x1 + (x0 - x1) / 2 if x0 > x1 else x0 + 3 * (x1 - x0) / 4, HEIGHT - Y_TRAIETTORIA_TIRO
        self.listX = [x0, x1, x2]

        a = np.array([[x0 ** 2, x0, 1], [x1 ** 2, x1, 1], [x2 ** 2, x2, 1]])
        b = np.array([y0, y1, y2])
        sol = np.linalg.solve(a, b)
        self.a_b_c['a'] = sol[0]
        self.a_b_c['b'] = sol[1]
        self.a_b_c['c'] = sol[2]

    def tiro(self):
        if HEIGHT - self.onTiro['team tir'].yFrecciaTiro < 205:
            cBallInTiro = FERRO_1_CANESTRO_2 if self.onTiro['team tir'].nTeam == 1 else FERRO_1_CANESTRO_1
            self.onTiro['is rimb'] = True
        elif HEIGHT - self.onTiro['team tir'].yFrecciaTiro > 244:
            cBallInTiro = FERRO_2_CANESTRO_2 if self.onTiro['team tir'].nTeam == 1 else FERRO_2_CANESTRO_1
            self.onTiro['is rimb'] = True
        else:
            cBallInTiro = COORD_CANESTRO_2 if self.onTiro['team tir'].nTeam == 1 else COORD_CANESTRO_1
            self.onTiro['is can'] = True

        if self.onTiro['team tir'].nTeam == 1:
            if self.listX[0] < self.listX[1]:
                if self.x + SIZE_BALL[0] / 2 >= cBallInTiro[0]:
                    self.onTiro['in tiro'] = False
                elif self.x + self.onTiro['vel'] < cBallInTiro[0] - SIZE_BALL[0] / 2:
                    self.calcTraiettoria(self.x + self.onTiro['vel'])
                else:
                    self.x = cBallInTiro[0] - SIZE_BALL[0] / 2 - 6
                    self.calcTraiettoria(self.x + self.onTiro['vel'])
            elif self.x <= cBallInTiro[0]:
                self.onTiro['in tiro'] = False
            elif self.x - 6 > cBallInTiro[0] - SIZE_BALL[0] / 2 - 10:
                self.calcTraiettoria(self.x - 6)
            else:
                self.x = cBallInTiro[0] - SIZE_BALL[0] / 2 - 10
                self.calcTraiettoria(self.x - 6)
        elif self.listX[0] > self.listX[1]:  # si intende che sia l'altro team ad aver tirato
            if self.x <= cBallInTiro[0]:
                self.onTiro['in tiro'] = False
            elif self.x - self.onTiro['vel'] > cBallInTiro[0]:
                self.calcTraiettoria(self.x - self.onTiro['vel'])
            else:
                self.x = cBallInTiro[0]
                self.calcTraiettoria(self.x - self.onTiro['vel'])
        elif self.x >= cBallInTiro[0]:
            self.onTiro['in tiro'] = False
        elif self.x + 6 < cBallInTiro[0] - 10:
            self.calcTraiettoria(self.x + 6)
        else:
            self.x = cBallInTiro[0] - 10
            self.calcTraiettoria(self.x + 6)

    def prepRimbalzoFerro(self):
        x0, x1 = self.listX[0], self.listX[1]
        x0r = x1
        if self.onTiro['team tir'].nTeam == 1:
            if x1 > x0:
                x1r, x2r = x0 + (x1 - x0) / 2, x1 - (x1 - x0) / 4
            else:
                x1r, x2r = x0, x1 + (x0 - x1) / 2
        elif x0 > x1:
            x1r, x2r = x1 + (x0 - x1) / 2, x1 + (x1 - x0) / 4
        else:
            x1r, x2r = x0, x0 - (x0 - x1) / 2

        self.calcTraiettoria(x0r)
        y0r, y1r, y2r = self.y, self.yGiocCheTira + SIZE_BALL[1], HEIGHT - Y_RIM_FERRO
        self.listX = [x0r, x1r, x2r]

        a = np.array([[x0r ** 2, x0r, 1], [x1r ** 2, x1r, 1], [x2r ** 2, x2r, 1]])
        b = np.array([y0r, y1r, y2r])
        sol = np.linalg.solve(a, b)
        self.a_b_c['a'] = sol[0]
        self.a_b_c['b'] = sol[1]
        self.a_b_c['c'] = sol[2]

    def rimbalzoFerro(self):
        if not self.onTiro['calc rimb fatto']:
            self.prepRimbalzoFerro()
            self.onTiro['calc rimb fatto'] = True
        if self.listX[0] > self.listX[1]:
            if self.x <= self.listX[1]:
                self.onTiro['is rimb'] = False
                self.onTiro['calc rimb fatto'] = False
                self.isAlone = True
            elif self.x - self.onTiro['vel'] / 2 > self.listX[1]:
                self.calcTraiettoria(self.x - self.onTiro['vel'] / 2)
            else:
                self.x = self.listX[1]
                self.calcTraiettoria(self.x)
        else:
            if self.x >= self.listX[1]:
                self.onTiro['is rimb'] = False
                self.onTiro['calc rimb fatto'] = False
                self.isAlone = True
            elif self.x + self.onTiro['vel'] / 2 < self.listX[1]:
                self.calcTraiettoria(self.x + self.onTiro['vel'] / 2)
            else:
                self.x = self.listX[1]
                self.calcTraiettoria(self.x)

        self.isAlone = True

    def completeCanestro(self):
        if self.y == HEIGHT - Y_CANESTRI:
            self.onTiro['is can'] = False
            self.isAlone = True
        elif self.y - 35 > HEIGHT - Y_CANESTRI:
            self.y -= 35
        else:
            self.y = HEIGHT - Y_CANESTRI

    def preparazionePassaggio(self, gioc1, gioc2):
        self.onPassaggio['gPass'] = gioc1
        self.onPassaggio['gRicev'] = gioc2
        x1 = gioc2.x + 30 if gioc2.giratoDa == 'left' else gioc2.x + gioc2.imgFace['left'].get_width() + gioc2.imgHand['left'].get_width() - 30
        y1 = gioc2.y + gioc2.imgShoes['left'].get_height() + gioc2.imgHand['left'].get_height() - SIZE_BALL[1] / 2 if gioc2.giratoDa == 'left' else gioc2.y + gioc2.imgShoes['right'].get_height() + gioc2.imgHand['right'].get_height() - SIZE_BALL[1] / 2
        a = np.array([[self.x, 1], [x1, 1]])
        b = np.array([self.y, y1])

        sol = np.linalg.solve(a, b)
        self.m_q['m'] = sol[0]
        self.m_q['q'] = sol[1]

    def passaggio(self):
        g = self.onPassaggio['gRicev']
        x = g.x + 30 if g.giratoDa == 'left' else g.x + g.imgFace['left'].get_width() + g.imgHand['left'].get_width() - 30

        if self.x == x:
            self.onPassaggio['gPass'].selected = False
            self.onPassaggio['in pass'] = False
            g.haLaPalla = True
            g.selected = True
            self.onPalleggio['in pall'] = True
        elif self.x > x:
            if self.x - 23 > x:
                self.calcPassaggio(self.x - 23)
            else:
                self.calcPassaggio(x)
        elif self.x + 23 < x:
            self.calcPassaggio(self.x + 23)
        else:
            self.calcPassaggio(x)

    def calcTraiettoria(self, x):
        y = self.a_b_c['a'] * x * x + self.a_b_c['b'] * x + self.a_b_c['c']
        self.x = x
        self.y = y

    def calcPassaggio(self, x):
        y = self.m_q['m'] * x + self.m_q['q']
        self.x = x
        self.y = y


class Team:
    def __init__(self, n, name, listPl):
        self.name = name
        self.nTeam = n
        self.attackTo = 'right' if n == 1 else 'left'
        self.players = []
        self.imgTriangle = pygame.image.load('images/triangolo_bianco.png') if n == 1 else pygame.image.load('images/triangolo_verde.png')
        self.imgBarraTiro = pygame.image.load('images/barraTiro.png')
        self.imgFrecciaTiro = pygame.image.load('images/freccia_verde.png')
        self.isInSceltaTiro = False
        self.dirFrecciaTiro = 'up'
        self.yFrecciaTiro = HEIGHT - self.imgFrecciaTiro.get_height()
        self.giocCheHaTirato = None
        self.puntiGiaAgg = False
        self.puntiPartita = 0
        self.atStartAzione = False
        self.azPartita = False
        self.m_q_mov = {'m': 0, 'q': 0}
        self.cooMovimento = ()
        self.checkNMov = 0
        self.isDifesaIniz = False
        self.setGiocatori(listPl)
        self.velBarraTiro = 20

    def setGiocatori(self, pl):
        giocBianchi = ('anthony_davis.png', 'domantas_sabonis.png', 'giannis_antetokounmpo.png', 'james_harden.png', 'jason_tatum.png', 'lebron_james.png', 'steph_curry.png')
        for i, g in enumerate(pl):
            path = 'images/players/faces/' + g['path']
            if self.nTeam == 1:
                x = 600 if i == 0 else 400
            else:
                x = WIDTH - 800 if i == 0 else WIDTH - 600
            if i == 0:
                y = Y_CAMPO / 2 + Y_BORDO_2_CAMPO
            elif i == 1:
                y = 79.5
            else:
                y = 280
            self.players.append(Player(path, g['path'] in giocBianchi, self.nTeam, x, y, i == 0))

    def isInPossesso(self):
        for g in self.players:
            if g.haLaPalla:
                return True
        return False

    def setVelBarraTiro(self, x, y):
        if self.nTeam == 1:
            i = (abs(COORD_CANESTRO_2[0] - x) ** 2 + abs(y + 202 - HEIGHT) ** 2) ** .5
        else:
            i = (abs(COORD_CANESTRO_1[0] - x) ** 2 + abs(y + 202 - HEIGHT) ** 2) ** .5
        self.velBarraTiro = int(DEF_BARRA_TIRO['v'] * i / DEF_BARRA_TIRO['i'])

    def writeBarraTiro(self, ball, display):
        if self.isInSceltaTiro or (ball.onTiro['in tiro'] and ball.onTiro['team tir'] == self):
            hGeneric = HEIGHT - self.imgFrecciaTiro.get_height() / 2

            if self.nTeam == 1:
                display.blit(self.imgBarraTiro, (10, hGeneric - self.imgBarraTiro.get_height()))
            else:
                display.blit(self.imgBarraTiro, (WIDTH - 10 - self.imgBarraTiro.get_width(), hGeneric - self.imgBarraTiro.get_height()))

            if hGeneric - self.yFrecciaTiro <= 147 or hGeneric - self.yFrecciaTiro >= 262:
                freccia = pygame.image.load('images/freccia_grigia.png')
            elif 148 <= hGeneric - self.yFrecciaTiro <= 173 or 236 <= hGeneric - self.yFrecciaTiro <= 261:
                freccia = pygame.image.load('images/freccia_arancione.png')
            elif 174 <= hGeneric - self.yFrecciaTiro <= 185 or 224 <= hGeneric - self.yFrecciaTiro <= 235:
                freccia = pygame.image.load('images/freccia_gialla.png')
            else:
                freccia = pygame.image.load('images/freccia_verde.png')
            if self.nTeam == 2:
                freccia = pygame.transform.flip(freccia, True, False)

            if self.nTeam == 1:
                display.blit(freccia, (10 + self.imgBarraTiro.get_width(), self.yFrecciaTiro))
            else:
                display.blit(freccia, (WIDTH - 20 - self.imgBarraTiro.get_width() - freccia.get_width(), self.yFrecciaTiro))

            if self.dirFrecciaTiro == 'up' and self.isInSceltaTiro:
                if self.yFrecciaTiro - self.velBarraTiro <= HEIGHT - self.imgFrecciaTiro.get_height() / 2 - self.imgBarraTiro.get_height():
                    self.yFrecciaTiro = HEIGHT - self.imgFrecciaTiro.get_height() / 2 - self.imgBarraTiro.get_height()
                    self.dirFrecciaTiro = 'down'
                else:
                    self.yFrecciaTiro -= self.velBarraTiro
            elif self.isInSceltaTiro:
                if self.yFrecciaTiro + self.velBarraTiro >= HEIGHT - self.imgFrecciaTiro.get_height():
                    self.yFrecciaTiro = HEIGHT - self.imgFrecciaTiro.get_height()
                    self.dirFrecciaTiro = 'up'
                else:
                    self.yFrecciaTiro += self.velBarraTiro

    def aggiornaPunteggio(self):
        x, y, v = self.giocCheHaTirato.x, self.giocCheHaTirato.y, self.giocCheHaTirato.giratoDa
        if self.nTeam == 1:
            for d in LINEA_3_CAN_2:
                if int(d['y']) == int(y):
                    if (v == 'right' and x <= d['x']) or (v == 'left' and x <= d['x'] - 60):
                        self.puntiPartita += 3
                    else:
                        self.puntiPartita += 2
                    break
        else:
            for d in LINEA_3_CAN_1:
                if int(d['y']) == int(y):
                    if (v == 'left' and x >= d['x']) or (v == 'right' and x <= d['x'] - 60):
                        self.puntiPartita += 3
                    else:
                        self.puntiPartita += 2
                    break

    def setGiocCheHaTirato(self):
        for g in self.players:
            if g.selected:
                self.giocCheHaTirato = g
                return

    def creaMovimento(self):
        self.checkNMov = 1
        gConPalla, gInMovimento = None, None
        for g in self.players:
            if g.haLaPalla:
                gConPalla = g
        while gInMovimento is None:
            n = randint(0, len(self.players) - 1)
            if not self.players[n].haLaPalla:
                gInMovimento = self.players[n]

        if gConPalla is None:
            return

        gConPalla.x, gConPalla.y = int(gConPalla.x), int(gConPalla.y)  # casting per effettuare il movimento con più possibilità di successo
        x0, y0 = gInMovimento.x, gInMovimento.y
        x1 = gConPalla.x + 60 if gConPalla.x < x0 else gConPalla.x - 60
        y1 = gConPalla.y - 30 if y0 < gConPalla.y else gConPalla.y + 30

        a = np.array([[x0, 1], [x1, 1]])
        b = np.array([y0, y1])
        sol = np.linalg.solve(a, b)
        self.m_q_mov['m'] = sol[0]
        self.m_q_mov['q'] = sol[1]
        self.cooMovimento = (x1, y1)
        gInMovimento.inMovimento = True

    def inizioNewAzioneOff(self, ball: Ball):
        self.atStartAzione = True
        for g in self.players:
            g.nMovimenti = 0

        gPassatore = self.players[0]
        gPassatore.giratoDa = 'right' if self.nTeam == 1 else 'left'
        gRic = self.players[1]
        gOther = self.players[2]
        x0 = 0 if self.nTeam == 1 else WIDTH - gPassatore.imgFace['left'].get_width() - 80
        x1 = 250 if self.nTeam == 1 else WIDTH - gPassatore.imgFace['left'].get_width() - 400
        x2 = 200 if self.nTeam == 1 else WIDTH - gPassatore.imgFace['left'].get_width() - 350

        gPassatore.x = x0
        gPassatore.y = 79.5
        gPassatore.haLaPalla = True
        gPassatore.selected = True
        gPassatore.setObj_x_off(self)
        ball.isAlone = False
        ball.onPalleggio['in pall'] = False
        gRic.x = x1
        gRic.y = 169.5
        gRic.setObj_x_off(self, True)
        gRic.haLaPalla = False
        gRic.selected = False
        gOther.x = x2
        gOther.y = 274.5
        gOther.haLaPalla = False
        gOther.selected = False
        gOther.setObj_x_off(self)

    def inizioNewAzioneDif(self):
        self.isDifesaIniz = True
        for g in self.players:
            g.selected = False
            g.haLaPalla = False
            g.nMovimenti = 0
        gMetaCampo = self.players[0]
        gDifs = self.players[1:]
        xDifs = [350 if self.nTeam == 2 else WIDTH - 500, 300 if self.nTeam == 2 else WIDTH - gDifs[1].imgFace['left'].get_width() - 450]
        yDifs = [79.5, 274.5]

        gMetaCampo.x = WIDTH / 2 - gMetaCampo.imgFace['left'].get_width() / 2
        gMetaCampo.y = 169.5
        gMetaCampo.selected = True
        gMetaCampo.haLaPalla = False
        for g, x, y in zip(gDifs, xDifs, yDifs):
            g.x = x
            g.y = y
            g.setObj_x_dif(self)


class Player:
    def __init__(self, path, isWhite, team, x, y, selected):
        _face = pygame.image.load(path)
        _shoes = pygame.image.load('images/players/shoes.png')
        _hand = pygame.image.load('images/players/mano_bianca.png') if isWhite else pygame.image.load('images/players/mano_nera.png')
        _tShirt = pygame.image.load('images/players/maglia_1.png') if team == 1 else pygame.image.load('images/players/maglia_2.png')

        self.name = ' '.join(path[len('images/players/faces/'):-4].split('_')).title()
        self.imgFace = {'right': _face, 'left': pygame.transform.flip(_face, True, False)}
        self.imgShoes = {'right': _shoes, 'left': pygame.transform.flip(_shoes, True, False)}
        self.imgHand = {'right': _hand, 'left': pygame.transform.flip(_hand, True, False)}
        self.imgTshirt = {'right': _tShirt, 'left': pygame.transform.flip(_tShirt, True, False)}
        self.x = x
        self.y = y
        self.z = 0
        self.isWhite = isWhite
        self.selected = selected
        self.inSalto = False
        self.haLaPalla = False
        self.giratoDa = 'right' if team == 1 else 'left'
        self.giaMossa = False
        self.objX = None
        self.inMovimento = False
        self.nMovimenti = 0

    def __closeSaltoInPassaggio(self):
        if self.z > 0:
            self.z -= 9
        if self.z < 0:
            self.z = 0

    def updatePlayer(self, ball: Ball, verso, team: Team, startAz):
        if self.selected:
            if self.inSalto and self.z < 120:
                self.z += 9
                if self.haLaPalla:
                    ball.z += 9
                return
            elif self.inSalto and 120 < self.z < 135:
                self.z += 4.5
                if self.haLaPalla:
                    ball.z += 4.5
                return

            self.inSalto = False
            if not ball.onTiro['in tiro'] and not ball.onTiro['is can'] and not ball.onTiro['is rimb'] and not team.atStartAzione:
                ball.onPalleggio['in pall'] = True

            if self.haLaPalla:
                self.inMovimento = False

            if self.z > 0:
                self.z -= 9
                if self.haLaPalla:
                    ball.z -= 9
            elif self.z < 0:
                self.z = 0
                if self.haLaPalla:
                    ball.z = 0

            self.__setRecuperoPalla(ball)
            if not ball.onTiro['in tiro'] and not ball.onTiro['is rimb'] and not ball.onTiro['is can'] and self.haLaPalla:
                if verso == 'left':
                    ball.x = self.x + 30
                    ball.y = self.y + self.imgShoes['left'].get_height() + self.imgHand['left'].get_height() - SIZE_BALL[1] / 2
                else:
                    ball.x = self.x + self.imgFace['left'].get_width() + self.imgHand['left'].get_width() - 30
                    ball.y = self.y + self.imgShoes['right'].get_height() + self.imgHand['right'].get_height() - SIZE_BALL[1] / 2
                ball.palleggia()
        else:
            self.__setRecuperoPalla(ball)
            self.__closeSaltoInPassaggio()
            if self.inMovimento:
                self.__execMovimento(team)
                return
            if startAz and self.nMovimenti == 0 and ((not team.azPartita and not team.atStartAzione and self.objX is not None and not ball.onPassaggio['in pass']) or team.isDifesaIniz):
                if team.nTeam == 1:
                    if not team.isDifesaIniz:
                        self.x = self.x + 17 if self.x + 17 < self.objX else self.objX
                        self.giratoDa = 'right'
                    else:
                        self.x = self.x - 17 if self.x - 17 > self.objX else self.objX
                        self.giratoDa = 'left'
                else:
                    if team.isDifesaIniz:
                        self.x = self.x + 17 if self.x + 17 < self.objX else self.objX
                        self.giratoDa = 'right'
                    else:
                        self.x = self.x - 17 if self.x - 17 > self.objX else self.objX
                        self.giratoDa = 'left'

    def __execMovimento(self, team: Team):
        self.x, self.y = int(self.x), int(self.y)
        if (self.x, self.y) == team.cooMovimento:
            self.inMovimento = False
            team.checkNMov = 0
            self.nMovimenti += 1
        elif self.x > team.cooMovimento[0]:
            if self.x - 10 > team.cooMovimento[0]:
                self.x -= 10
                self.y = self.x * team.m_q_mov['m'] + team.m_q_mov['q']
            else:
                self.x, self.y = team.cooMovimento[0], team.cooMovimento[1]
        elif self.x + 10 < team.cooMovimento[0]:
            self.x += 10
            self.y = self.x * team.m_q_mov['m'] + team.m_q_mov['q']
        else:
            self.x, self.y = team.cooMovimento[0], team.cooMovimento[1]

    def setObj_x_off(self, team: Team, isRicevitore=False):
        if isRicevitore:
            self.objX = 850 if team.nTeam == 1 else WIDTH - 950
        else:
            self.objX = 950 if team.nTeam == 1 else WIDTH - 1150

    def setObj_x_dif(self, team: Team):
        self.objX = 1050 if team.nTeam == 2 else WIDTH - 1250

    def __setRecuperoPalla(self, ball: Ball):
        if not ball.isAlone:
            return

        xB, yB = ball.x, ball.y + ball.z
        verso = self.giratoDa
        img1 = self.imgFace[verso]
        img3 = self.imgShoes[verso]
        img4 = self.imgHand[verso]

        if ball.onTiro['is rimb'] and HEIGHT - ball.listX[1] + SIZE_BALL[1] - 10 <= self.y <= HEIGHT - ball.listX[1] + SIZE_BALL[1]:
            return

        if not int(self.y + self.z) <= int(yB - SIZE_BALL[1]) <= int(self.y + self.z + img3.get_height() + img4.get_height() - SIZE_BALL[1] / 2):
            return
        if self.giratoDa == 'right':
            if self.x + img1.get_width() - img4.get_width() / 1.5 + 15 <= xB <= self.x + img1.get_width() - img4.get_width() / 1.5 + 15 + img4.get_width() / 2:
                self.haLaPalla = True
                ball.isAlone = False
                ball.onPalleggio['in pall'] = True
                ball.onPalleggio['verso alto'] = True
                ball.palleggia()
        elif self.x + img1.get_width() - img4.get_width() / 4 - 35 <= xB <= self.x + img1.get_width() - img4.get_width() / 4 - 15:  # sottinteso che self.giratoDa == 'left'
            self.haLaPalla = True
            ball.isAlone = False
            ball.onPalleggio['in pall'] = True
            ball.onPalleggio['verso alto'] = True
            ball.palleggia()

    def drawPlayer(self, display, triangolo):
        img1 = self.imgFace[self.giratoDa]
        img2 = self.imgTshirt[self.giratoDa]
        img3 = self.imgShoes[self.giratoDa]
        img4 = self.imgHand[self.giratoDa]

        if self.giratoDa == 'right':
            display.blit(img2, (self.x + (img1.get_width() - img2.get_width()) / 2 + 5, HEIGHT - self.y - img3.get_height() - img2.get_height() + 10 - self.z))
            display.blit(img1, (self.x, HEIGHT - self.y - img3.get_height() - img2.get_height() - img1.get_height() + 26 - self.z))
            if self.selected:
                display.blit(triangolo, (self.x + (img1.get_width() - triangolo.get_width()) / 2, HEIGHT - self.y - img3.get_height() - img2.get_height() - img1.get_height() - 20 - self.z))
            if self.inSalto:
                newShoes = pygame.image.load('images/players/shoesInSalto.png') if self.giratoDa == 'right' else pygame.transform.flip(pygame.image.load('images/players/shoesInSalto.png'), True, False)
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
                newShoes = pygame.image.load('images/players/shoesInSalto.png') if self.giratoDa == 'right' else pygame.transform.flip(pygame.image.load('images/players/shoesInSalto.png'), True, False)
                display.blit(newShoes, (self.x + img1.get_width(), HEIGHT - self.y - img3.get_height() - self.z - 5))
                newHand = pygame.transform.flip(pygame.image.load('images/players/mano_bianca_inSalto.png') if self.isWhite else pygame.image.load('images/players/mano_nera_inSalto.png'), True, False)
                display.blit(newHand, (self.x + img1.get_width() - img4.get_width() / 4, HEIGHT - self.y - img3.get_height() - newHand.get_height() - self.z))
            else:
                display.blit(img3, (self.x + img1.get_width(), HEIGHT - self.y - img3.get_height() - self.z))
                display.blit(img4, (self.x + img1.get_width() - img4.get_width() / 4 - 15, HEIGHT - self.y - img3.get_height() - img4.get_height() - self.z - 20))


def main():
    pygame.init()
    window = FirstWindow()
    rules = SecondWindow(window.display, window.inpName_1['text'], window.inpName_2['text'])
    game = Game(window.display, window.inpName_1['text'], window.inpName_2['text'], window.listPlayers)

    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if window.inSchermataIniz:
                window.checkEvt(e)
            elif e.type == KEYDOWN and not rules.inSchermataRegole:
                game.checkAzioniTeam_1(e.key)
                game.checkAzioniTeam_2(e.key)
            else:
                rules.checkEvt(e)

        if window.inSchermataIniz:
            window.updateWindow()
        elif not rules.inSchermataRegole:
            game.checkMovimentiTeam_1()
            game.checkMovimentiTeam_2()
            game.reloadWindow()

        if not window.inSchermataIniz and rules.inSchermataRegole:
            rules.updateWindow()

        pygame.time.Clock().tick(FPS)
        pygame.display.update()


if __name__ == '__main__':
    main()
