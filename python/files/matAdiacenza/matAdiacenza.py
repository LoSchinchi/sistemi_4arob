import pygame as pg
from pygame.locals import *
import sys

DIM_CASELLA = 100

def getDim(c):
    t = 0
    for l in c:
        t += l.count('0')
    return t

def main():
    fp = open('matAdiacenza.csv', 'r')
    celle = [line.split(',') for line in fp.readlines()]
    fp.close()
    for c in celle:
        c[-1] = c[-1][0]

    print(celle)
    dim = getDim(celle)
    tab = []
    n = 0
    for line in celle:
        newTab = []
        for c in line:
            if c == '1':
                newTab.append(-1)
            else:
                newTab.append(n)
                n += 1
        tab.append(newTab)
    print(tab)

    tabTutto = []
    for i, line in enumerate(tab):
        for j, c in enumerate(line):
            celleAd = []
            if c == -1:
                continue

            if j != 0 and tab[i][j-1] != -1:
                celleAd.append(tab[i][j-1])
            if j != len(line) - 1 and tab[i][j + 1] != -1:
                celleAd.append(tab[i][j + 1])
            if i != 0 and tab[i - 1][j] != -1:
                celleAd.append(tab[i - 1][j])
            if i != len(tab) - 1 and tab[i + 1][j] != -1:
                celleAd.append(tab[i + 1][j])

            tabTutto.append([1 if k in celleAd else 0 for k in range(dim)])
    
    print("tab def:")
    for l in tabTutto:
        print(l)

    pg.init()
    screen = pg.display.set_mode((len(celle) * DIM_CASELLA, len(celle) * DIM_CASELLA))

    while True:
        for e in pg.event.get():
            if e.type == QUIT:
                pg.quit()
                sys.exit()
        for i, line in enumerate(celle):
            for j, n in enumerate(line):
                sur = pg.Surface((DIM_CASELLA, DIM_CASELLA))
                sur.fill('white' if n == '0' else 'black')
                screen.blit(sur, pg.Rect(j * DIM_CASELLA, i * DIM_CASELLA, DIM_CASELLA, DIM_CASELLA))

        pg.time.Clock().tick(50)
        pg.display.update()


if __name__ == '__main__':
    main()