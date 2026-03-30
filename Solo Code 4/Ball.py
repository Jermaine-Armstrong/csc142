# Originally by Irv Kalb from Chapter 6 of Object-Oriented Python
# Modified by David Kopec to move in an arc

import pygame
from pygame.locals import *
import random
from math import sin

# Ball class 
class Ball():

    def __init__(self, window, windowWidth, windowHeight):
        self.window = window  # remember the window, so we can draw later
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        self.image = pygame.image.load('images/ball.png')
        # A rect is made up of [x, y, width, height]
        self.ballRect = self.image.get_rect()
        self.width = self.ballRect.width
        self.height = self.ballRect.height
        self.maxWidth = windowWidth - self.width
        self.maxHeight = windowHeight - self.height
        
        # Pick a random starting position 
        self.x = random.randrange(0, self.maxWidth)
        self.y = self.height

        # Choose a random speed between -4 and 4, but not zero
        # in both the x and y directions
        speedsList = [-7, -6, -5, -4, -3, 3, 4, 5, 6, 7] 
        self.xSpeed = random.choice(speedsList)
        self.ySpeed = random.randrange(self.maxHeight, self.windowHeight * 2)

    def update(self):
        # Check for hitting a wall.  If so, change that direction.
        if (self.x < -self.width) or (self.x >= self.windowWidth):
            self.xSpeed = -self.xSpeed

        # Update the Ball's x and y, using the speed in two directions
        self.x = self.x + self.xSpeed
        self.y = self.windowWidth - self.ySpeed * sin(3.14 * self.x / self.maxWidth)
        self.ballRect.x = self.x
        self.ballRect.y = self.y

    def draw(self):
        self.window.blit(self.image, (self.x, self.y))
