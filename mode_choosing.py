import random
import time
import pygame
import game_mechanism
import button
from overwriteUI import *
from assets import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Wordle")
font = pygame.font.Font(FONT,55)
medium_font = pygame.font.Font(FONT,35)
small_font = pygame.font.Font(FONT,18)
back_img = pygame.image.load("images/button_img/left_arrow.png")
EN_img = pygame.image.load("images/button_img/EN.png")
VI_img = pygame.image.load("images/button_img/VI.png")
EQ_img = pygame.image.load("images/button_img/EQ.png")

game_enter_sfx = pygame.mixer.Sound("sound/game_enter.mp3")
game_enter_sfx.set_volume(0.3)
popup_timer = 0
popup_msg = ""

option_height = 50
option_width = 350
Options = [button.OptionButton(350, 135 + 25/2, option_width, option_height, "5 Ký tự", "EN", 5, small_font),
           button.OptionButton(350, 135 + 25/2 + option_height + 25, option_width, option_height, "6 Ký tự", "EN", 6, small_font),
           
           button.OptionButton(350, 385, option_width, option_height, "6 Ký tự", "VI", 6, small_font),
           button.OptionButton(350, 385 + option_height + 25, option_width, option_height, "7 Ký tự", "VI", 7, small_font),
           button.OptionButton(350, 385 + 2 * (option_height + 25), option_width, option_height, "8 Ký tự", "VI", 8, small_font),
              
           button.OptionButton(350, 685 + 25/2, option_width, option_height, "7 Ký tự", "Equation", 7, small_font),
           button.OptionButton(350, 685 + 25/2 + option_height + 25, option_width, option_height, "8 Ký tự", "Equation", 8, small_font)]
def draw_gamemode_button(manager):
    mouse_pos = pygame.mouse.get_pos()
    mode_sqr_size = 200

    EN_surface =  pygame.transform.scale(EN_img, (mode_sqr_size, mode_sqr_size))
    EN_rect = EN_surface.get_rect(center = (200,210))
    screen.blit(EN_surface,EN_rect)

    VI_surface =  pygame.transform.scale(VI_img, (mode_sqr_size, mode_sqr_size))
    VI_rect = EN_surface.get_rect(center = (200,485))
    screen.blit(VI_surface,VI_rect)

    EQ_surface =  pygame.transform.scale(EQ_img, (mode_sqr_size, mode_sqr_size))
    EQ_rect = EQ_surface.get_rect(center = (200,760))
    screen.blit(EQ_surface,EQ_rect)
    

    #Hiển thị các option
    for option in Options:
        if option.rect.collidepoint(mouse_pos) and pygame.mouse.get_just_released()[0]:
            if option.ischosen == True:
                option.ischosen = False
            else:
                for op in Options:
                    op.ischosen = False
                option.ischosen = True
        option.draw(screen)

def confirm_button(manager):
    confirm_butt = button.TextButton(250,SCREEN_HEIGHT-25-75 ,300, 75, "XÁC  NHẬN", medium_font, False)
    confirm_butt.draw(screen)
    mouse_pos = pygame.mouse.get_pos()
    if confirm_butt.rect.collidepoint(mouse_pos) and pygame.mouse.get_just_released()[0]:
        for option in Options:
            if option.ischosen:
                if manager.data_manager.current_user.is_practice_mode:
                    option.ischosen = False
                    manager.game = game_mechanism.Game(option.value,option.mode)
                    manager.data_manager.current_user.is_updated = False
                    print(manager.game.secret_word,1)
                    manager.state = "Game Play"
                    if manager.sfx:
                        game_enter_sfx.play()
                    break
                else:
                    if manager.data_manager.current_user.ranked_lives > 0:
                        manager.data_manager.current_user.ranked_lives -= 1

                        if manager.data_manager.current_user.ranked_lives == 2:
                            manager.data_manager.current_user.last_life_regen = time.time()

                        option.ischosen = False
                        manager.game = game_mechanism.Game(option.value,option.mode)
                        manager.game.type = "RANK"
                        manager.data_manager.current_user.is_updated = False
                        print(manager.game.secret_word,1)
                        manager.state = "Game Play"
                        if manager.sfx:
                            game_enter_sfx.play()
                        break
                    else:
                        no_lives_popup(manager)
def no_lives_popup(manager):
    global popup_timer, popup_msg
    popup_timer = pygame.time.get_ticks() + 1500
    popup_msg = "Bạn đã hết lượt chơi"

def draw_no_lives_pop_up():
    if pygame.time.get_ticks() < popup_timer:
        text_surf = font30.render(popup_msg, True, BLACK)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        bg_rect = text_rect.inflate(20, 15)
        pygame.draw.rect(screen, WHITE, bg_rect, border_radius=5)
        pygame.draw.rect(screen, GREY, bg_rect, 3, border_radius=5)
        screen.blit(text_surf, text_rect)
def back2mainmenu_button(manager):
    cb_button = button.ImgButton(SCREEN_WIDTH-25-50/2,SCREEN_HEIGHT-25-50/2,back_img,50,50, manager.sfx)
    cb_button.draw_button()

    mouse_pos = pygame.mouse.get_pos()
    if cb_button.rect.collidepoint(mouse_pos) and pygame.mouse.get_just_released()[0]:
        manager.state = "Main Menu"
def mode_choosing_title(manager):
    title_surface = font.render(f'Chọn Chế Độ', True, BLACK)
    title_rect = title_surface.get_rect(center = (SCREEN_WIDTH // 2, 50))
    screen.blit(title_surface,title_rect)
def draw_mode_choosing(manager):
    draw_gamemode_button(manager)
    confirm_button(manager)
    back2mainmenu_button(manager)
    mode_choosing_title(manager)
    draw_no_lives_pop_up()
    if manager.overwrite_noti:
        draw_overwrite_noti(screen, manager)