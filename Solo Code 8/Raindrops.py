import pygame
from pygame.locals import *
import sys
import random


BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30


class Raindrop:
    __slots__ = ["x", "y", "radius"]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 1

    def update(self):
        self.radius += 1

    def draw(self, window):
        pygame.draw.circle(window, BLUE, (self.x, self.y), self.radius, 1)


class RaindropsManager:
    RAIN_RATE = 300
    MAX_RADIUS = 35

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.raindrops = []
        self.last_drop_time = pygame.time.get_ticks()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            current_time = pygame.time.get_ticks()
            if current_time - self.last_drop_time >= self.RAIN_RATE:
                x = random.randint(0, WINDOW_WIDTH)
                y = random.randint(0, WINDOW_HEIGHT)
                self.raindrops.append(Raindrop(x, y))
                self.last_drop_time = current_time

            for raindrop in self.raindrops:
                raindrop.update()

            self.raindrops = [raindrop for raindrop in self.raindrops
                              if raindrop.radius <= self.MAX_RADIUS]

            self.window.fill(BLACK)

            for raindrop in self.raindrops:
                raindrop.draw(self.window)

            pygame.display.update()
            self.clock.tick(FRAMES_PER_SECOND)


raindrops_manager = RaindropsManager()
raindrops_manager.run()
