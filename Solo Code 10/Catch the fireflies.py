import math
import random
import sys
import pygame
import pygwidgets

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
FRAMES_PER_SECOND = 60
BACKGROUND_COLOR = (10, 16, 38)
TITLE_COLOR = (255, 245, 170)
TEXT_COLOR = (235, 240, 255)
BUTTON_COLOR = (210, 220, 255)


class Firefly:
    def __init__(self):
        self.radius = random.randint(14, 26)
        self.x = random.randint(self.radius, WINDOW_WIDTH - self.radius)
        self.y = random.randint(140, WINDOW_HEIGHT - self.radius)
        self.dx = random.choice([-1, 1]) * random.uniform(1.4, 3.0)
        self.dy = random.choice([-1, 1]) * random.uniform(1.0, 2.4)
        self.phase = random.uniform(0, math.tau)
        self.phase_speed = random.uniform(0.08, 0.16)
        self.color = random.choice([(255, 228, 110), (180, 255, 140), (255, 190, 110)])

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.phase += self.phase_speed

        if self.x <= self.radius or self.x >= WINDOW_WIDTH - self.radius:
            self.dx *= -1
        if self.y <= 140 or self.y >= WINDOW_HEIGHT - self.radius:
            self.dy *= -1

    def draw(self, window):
        glow_radius = self.radius + int(8 + 6 * math.sin(self.phase))
        glow_surface = pygame.Surface((glow_radius * 4, glow_radius * 4), pygame.SRCALPHA)
        center = glow_radius * 2
        pygame.draw.circle(glow_surface, (*self.color, 40), (center, center), glow_radius + 10)
        pygame.draw.circle(glow_surface, (*self.color, 90), (center, center), glow_radius)
        window.blit(glow_surface, (self.x - center, self.y - center))
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(window, (255, 255, 255), (int(self.x), int(self.y)), self.radius // 3)

    def was_clicked(self, position):
        mouse_x, mouse_y = position
        return math.hypot(mouse_x - self.x, mouse_y - self.y) <= self.radius + 6


class Spark:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.uniform(-3.5, 3.5)
        self.dy = random.uniform(-3.5, 3.5)
        self.size = random.randint(4, 8)
        self.life = random.randint(18, 32)
        self.color = random.choice([(255, 240, 120), (255, 200, 120), (200, 255, 170)])

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.08
        self.life -= 1

    def draw(self, window):
        if self.life > 0:
            alpha = max(20, min(255, self.life * 8))
            surface = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*self.color, alpha), (self.size * 2, self.size * 2), self.size)
            window.blit(surface, (self.x - self.size * 2, self.y - self.size * 2))


def make_gradient_background(window):
    for y in range(WINDOW_HEIGHT):
        blend = y / WINDOW_HEIGHT
        red = int(10 + 20 * blend)
        green = int(16 + 40 * blend)
        blue = int(38 + 55 * blend)
        pygame.draw.line(window, (red, green, blue), (0, y), (WINDOW_WIDTH, y))


def reset_game():
    fireflies = []
    sparks = []
    for _ in range(5):
        fireflies.append(Firefly())
    return fireflies, sparks, 0, pygame.time.get_ticks(), pygame.time.get_ticks(), True


pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Firefly Catch')
clock = pygame.time.Clock()
star_positions = []
for _ in range(40):
    star_positions.append((
        random.randint(0, WINDOW_WIDTH),
        random.randint(0, WINDOW_HEIGHT),
        random.randint(1, 3)
    ))

title_text = pygwidgets.DisplayText(window, (25, 20), 'Firefly Catch', fontSize=42, textColor=TITLE_COLOR)
instructions_text = pygwidgets.DisplayText(
    window, (25, 70), 'Click the moving fireflies before time runs out.',
    fontSize=24, textColor=TEXT_COLOR
)
score_text = pygwidgets.DisplayText(window, (25, 110), 'Score: 0', fontSize=28, textColor=TEXT_COLOR)
timer_text = pygwidgets.DisplayText(window, (250, 110), 'Time Left: 30', fontSize=28, textColor=TEXT_COLOR)
message_text = pygwidgets.DisplayText(window, (25, 555), '', fontSize=24, textColor=TITLE_COLOR)
restart_button = pygwidgets.TextButton(window, (730, 30), 'Restart', width=120, height=45, textColor=BUTTON_COLOR)

game_length = 30
spawn_delay = 700
fireflies, sparks, score, start_time, last_spawn_time, playing = reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if restart_button.handleEvent(event):
            fireflies, sparks, score, start_time, last_spawn_time, playing = reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and playing:
            click_hit = False
            for one_firefly in fireflies[:]:
                if one_firefly.was_clicked(event.pos):
                    score += 1
                    for _ in range(14):
                        sparks.append(Spark(one_firefly.x, one_firefly.y))
                    fireflies.remove(one_firefly)
                    fireflies.append(Firefly())
                    click_hit = True
                    break
            if not click_hit and score > 0:
                score -= 1

    current_time = pygame.time.get_ticks()
    seconds_passed = (current_time - start_time) // 1000
    time_left = max(0, game_length - seconds_passed)

    if playing and current_time - last_spawn_time >= spawn_delay:
        if len(fireflies) < 12:
            fireflies.append(Firefly())
        last_spawn_time = current_time

    if time_left == 0:
        playing = False

    if playing:
        message_text.setValue('Catch as many as you can. Missing a click loses 1 point.')
    else:
        message_text.setValue(f'Time is up. Final score: {score}. Press Restart to play again.')

    score_text.setValue(f'Score: {score}')
    timer_text.setValue(f'Time Left: {time_left}')

    for one_firefly in fireflies:
        if playing:
            one_firefly.update()

    for one_spark in sparks[:]:
        one_spark.update()
        if one_spark.life <= 0:
            sparks.remove(one_spark)

    make_gradient_background(window)

    for star_x, star_y, star_size in star_positions:
        pygame.draw.circle(window, (220, 230, 255), (star_x, star_y), star_size)

    pygame.draw.rect(window, (20, 28, 58), (0, 0, WINDOW_WIDTH, 145))
    pygame.draw.line(window, (255, 220, 120), (0, 145), (WINDOW_WIDTH, 145), 2)

    for one_firefly in fireflies:
        one_firefly.draw(window)

    for one_spark in sparks:
        one_spark.draw(window)

    title_text.draw()
    instructions_text.draw()
    score_text.draw()
    timer_text.draw()
    message_text.draw()
    restart_button.draw()

    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)
