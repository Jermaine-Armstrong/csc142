import pygame
from pygame.locals import *
import sys
from Ball import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30


def draw_text(surface, text, x, y, color, font_size=24):
    text_font = pygame.font.SysFont(None, font_size)
    text_surface = text_font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)


pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

ball_list = [Ball(window, WINDOW_WIDTH, WINDOW_HEIGHT) for _ in range(3)]
score = 0
start_ticks = pygame.time.get_ticks()
last_seconds = 0
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_pos = event.pos
            for i in range(len(ball_list) - 1, -1, -1):
                if ball_list[i].ballRect.collidepoint(mouse_pos):
                    del ball_list[i]
                    score += 1
                    break

    current_ticks = pygame.time.get_ticks()
    elapsed_seconds = (current_ticks - start_ticks) // 1000

    if not game_over and elapsed_seconds > last_seconds:
        for _ in range(elapsed_seconds - last_seconds):
            ball_list.append(Ball(window, WINDOW_WIDTH, WINDOW_HEIGHT))
        last_seconds = elapsed_seconds

    if not game_over and elapsed_seconds >= 15:
        game_over = True
        ball_list.clear()

    if not game_over:
        for ball in ball_list:
            ball.update()

    window.fill(BLACK)

    for ball in ball_list:
        ball.draw()

    draw_text(window, f"Score: {score}", 10, 10, WHITE, 28)
    draw_text(window, f"Seconds: {elapsed_seconds}", 10, 40, WHITE, 24)

    if game_over:
        draw_text(window, "Game Over", 220, 200, WHITE, 40)
        draw_text(window, f"Final Score: {score}", 210, 250, WHITE, 28)

    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)
