import pygame
from pygame.locals import *
import sys
import pygwidgets

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

O_TITLE = pygwidgets.DisplayText(window, (20, 20), 'Temperature Converter',
                                 fontSize=36, textColor=WHITE)

O_INPUT_LABEL = pygwidgets.DisplayText(window, (20, 90), 'Enter a temperature:',
                                       fontSize=24, textColor=WHITE)
O_INPUT_FIELD = pygwidgets.InputText(window, (20, 125), '',
                                     fontSize=24, textColor=BLACK, backgroundColor=WHITE, width=200)

O_F_TO_C_RADIO = pygwidgets.TextRadioButton(window, (20, 180), 'tempScale', 'Fahrenheit to Celsius',
                                            value=True, nickname='F_TO_C')
O_C_TO_F_RADIO = pygwidgets.TextRadioButton(window, (20, 210), 'tempScale', 'Celsius to Fahrenheit',
                                            value=False, nickname='C_TO_F')
O_F_TO_C_LABEL = pygwidgets.DisplayText(window, (45, 180), 'to Celsius',
                                        fontSize=24, textColor=WHITE)
O_C_TO_F_LABEL = pygwidgets.DisplayText(window, (45, 210), 'to Fahrenheit',
                                        fontSize=24, textColor=WHITE)

O_CONVERT_BUTTON = pygwidgets.TextButton(window, (20, 260), 'Convert')

O_OUTPUT_TEXT = pygwidgets.DisplayText(window, (20, 320), '',
                                       fontSize=28, textColor=WHITE)
O_MESSAGE_TEXT = pygwidgets.DisplayText(window, (20, 370), '',
                                        fontSize=20, textColor=WHITE)


def convert_temperature():
    raw_text = O_INPUT_FIELD.getValue().strip()
    if raw_text == '':
        O_OUTPUT_TEXT.setValue('')
        O_MESSAGE_TEXT.setValue('Please enter a number.')
        return

    try:
        temp_value = float(raw_text)
    except ValueError:
        O_OUTPUT_TEXT.setValue('')
        O_MESSAGE_TEXT.setValue('Please enter a valid number.')
        return

    selected = O_F_TO_C_RADIO.getSelectedRadioButton()
    if selected == 'F_TO_C':
        result = (temp_value - 32) / (9 / 5)
        O_OUTPUT_TEXT.setValue(f'Result: {result:.2f} C')
    else:
        result = (temp_value * 9 / 5) + 32
        O_OUTPUT_TEXT.setValue(f'Result: {result:.2f} F')

    O_MESSAGE_TEXT.setValue('')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if O_INPUT_FIELD.handleEvent(event):
            convert_temperature()

        if O_F_TO_C_RADIO.handleEvent(event):
            convert_temperature()

        if O_C_TO_F_RADIO.handleEvent(event):
            convert_temperature()

        if O_CONVERT_BUTTON.handleEvent(event):
            convert_temperature()

    window.fill(BLACK)

    O_TITLE.draw()
    O_INPUT_LABEL.draw()
    O_INPUT_FIELD.draw()
    O_F_TO_C_RADIO.draw()
    O_C_TO_F_RADIO.draw()
    O_F_TO_C_LABEL.draw()
    O_C_TO_F_LABEL.draw()
    O_CONVERT_BUTTON.draw()
    O_OUTPUT_TEXT.draw()
    O_MESSAGE_TEXT.draw()

    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)
