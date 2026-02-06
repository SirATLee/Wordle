import pygame
from gameplayUI import*
from main_menu import *
from mode_choosing import *
from top20_list import *
from assets import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Wordle")
font = pygame.font.Font(FONT,55)
def draw(manager):
    screen.fill(manager.theme)
    if manager.state == "Main Menu":
        draw_main_menu(manager)

    elif manager.state == "Mode Choosing":
        draw_mode_choosing(manager)
    elif manager.state == "Top-20 List":
        draw_top20_list(manager)

    elif manager.state == "Game Play":
        draw_gameplay(manager)