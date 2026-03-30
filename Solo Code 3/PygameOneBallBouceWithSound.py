import pygame
from pygame.locals import *
import sys
import random

BLACK = (0, 0, 0)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30
N_PIXELS_PER_FRAME = 3
TARGET_SCORE = 5

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
 
ballImage = pygame.image.load('images/ball.png')
bounceSound = pygame.mixer.Sound('sounds/boing.wav')
pygame.mixer.music.load('sounds/background.mp3')
pygame.mixer.music.play(-1, 0.0)
successSound = pygame.mixer.Sound('sounds/boing.wav')


def draw_text(surface, text, x, y, color, font_size=24):
    text_font = pygame.font.SysFont(None, font_size)
    text_surface = text_font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)


def reset_ball(rect, max_width, max_height):
    rect.left = random.randrange(max_width)
    rect.top = random.randrange(max_height)
    return rect


def increased_speed(speed):
    increase = random.randint(1, 5)
    if speed >= 0:
        return abs(speed) + increase
    return -(abs(speed) + increase)

ballRect = ballImage.get_rect()
MAX_WIDTH = WINDOW_WIDTH - ballRect.width
MAX_HEIGHT = WINDOW_HEIGHT - ballRect.height
ballRect.left = random.randrange(MAX_WIDTH)
ballRect.top = random.randrange(MAX_HEIGHT)
xSpeed = N_PIXELS_PER_FRAME
ySpeed = N_PIXELS_PER_FRAME
score = 0
gameOver = False
startTicks = pygame.time.get_ticks()
elapsedSeconds = None
lastClickPos = None
 
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if (event.type == pygame.MOUSEBUTTONDOWN) and (not gameOver):
            lastClickPos = event.pos
            if ballRect.collidepoint(event.pos):
                score += 1
                successSound.play()
                ballRect = reset_ball(ballRect, MAX_WIDTH, MAX_HEIGHT)
                xSpeed = increased_speed(xSpeed)
                ySpeed = increased_speed(ySpeed)
                if score >= TARGET_SCORE:
                    gameOver = True
                    elapsedSeconds = (pygame.time.get_ticks() - startTicks) / 1000.0
    
    if not gameOver:
        if (ballRect.left < 0) or (ballRect.right >= WINDOW_WIDTH):
            xSpeed = -xSpeed 
            bounceSound.play()

        if (ballRect.top < 0) or (ballRect.bottom >= WINDOW_HEIGHT):
            ySpeed = -ySpeed
            bounceSound.play()

        ballRect.left = ballRect.left + xSpeed
        ballRect.top = ballRect.top + ySpeed

    window.fill(BLACK)
    
    if not gameOver:
        window.blit(ballImage, ballRect)
    draw_text(window, f"Score: {score}", 10, 10, (255, 255, 255), 24)
    if gameOver and (elapsedSeconds is not None):
        message = f"You win! Time: {elapsedSeconds:.2f} seconds"
        message_font = pygame.font.SysFont(None, 36)
        message_surface = message_font.render(message, True, (255, 255, 255))
        message_rect = message_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        window.blit(message_surface, message_rect)

    pygame.display.update()

    clock.tick(FRAMES_PER_SECOND)
