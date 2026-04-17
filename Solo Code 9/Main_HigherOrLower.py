import pygame
from pygame.locals import *
import sys
import pygwidgets
from Game import *


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
FRAMES_PER_SECOND = 30


pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

background = pygwidgets.Image(window, (0, 0), 'images/background.png')
newGameButton = pygwidgets.TextButton(window, (20, 530), 'New Game', width=110, height=45)
stayButton = pygwidgets.TextButton(window, (360, 520), 'Stay', width=120, height=55)
hitButton = pygwidgets.TextButton(window, (520, 520), 'Hit', width=120, height=55)
quitButton = pygwidgets.TextButton(window, (880, 530), 'Quit', width=100, height=45)

oGame = Game(window)

while True:
    for event in pygame.event.get():
        if ((event.type == QUIT) or
                ((event.type == KEYDOWN) and (event.key == K_ESCAPE)) or
                quitButton.handleEvent(event)):
            pygame.quit()
            sys.exit()

        if newGameButton.handleEvent(event):
            oGame.reset()
            hitButton.enable()
            stayButton.enable()

        if hitButton.handleEvent(event):
            roundOver = oGame.hit()
            if roundOver:
                hitButton.disable()
                stayButton.disable()

        if stayButton.handleEvent(event):
            roundOver = oGame.stay()
            if roundOver:
                hitButton.disable()
                stayButton.disable()

    background.draw()
    oGame.draw()
    newGameButton.draw()
    stayButton.draw()
    hitButton.draw()
    quitButton.draw()

    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)
