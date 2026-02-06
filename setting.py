import pygame
import sys
import button
import base64
from assets import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Wordle")
playbut_img = pygame.image.load("images/button_img/test_button.png")
font = pygame.font.Font(FONT,55)
font18 = pygame.font.Font(FONT,18)
font20 = pygame.font.Font(FONT,20)
font22 = pygame.font.Font(FONT,22)
font24 = pygame.font.Font(FONT,24)
font26 = pygame.font.Font(FONT,26)
font28 = pygame.font.Font(FONT,28)
font30 = pygame.font.Font(FONT,30)
font32 = pygame.font.Font(FONT,32)
font40 = pygame.font.Font(FONT,40)
font45 = pygame.font.Font(FONT,45)
font50 = pygame.font.Font(FONT,50)
font60 = pygame.font.Font(FONT,60)
def draw_sub_setting(manager):
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    sub_setting_width = 300
    sub_setting_height = 360
    sub_setting_rect = pygame.Rect(0,0,sub_setting_width,sub_setting_height)
    sub_setting_rect.center = (SCREEN_WIDTH // 2, 430)
    pygame.draw.rect(screen, (10, 20, 30), sub_setting_rect, border_radius= 15)
    if sub_setting_rect.collidepoint(mouse_pos):
        color_border = NEON_GREEN
    else:
        color_border = GREY
    pygame.draw.rect(screen, color_border, sub_setting_rect, 3, border_radius= 15)

    button_width = 200
    button_height = 85
    resume_button = button.TextButton(SCREEN_WIDTH // 2 - button_width /2, 325 - button_height / 2, button_width, button_height,"Tiếp Tục", font32, manager.sfx)
    setting_button = button.TextButton(SCREEN_WIDTH // 2 - button_width /2, 430 - button_height / 2, button_width, button_height,"Cài Đặt", font32, manager.sfx)
    leave_button = button.TextButton(SCREEN_WIDTH // 2 - button_width /2, 535 - button_height / 2, button_width, button_height,"Thoát", font32, manager.sfx)
    resume_button.draw(screen)
    setting_button.draw(screen)
    leave_button.draw(screen)

    mouse_pos = pygame.mouse.get_pos()
    if pygame.mouse.get_just_released()[0]:
        if resume_button.rect.collidepoint(mouse_pos):
            manager.sub_setting = False
        elif setting_button.rect.collidepoint(mouse_pos):
            manager.setting = True
            manager.sub_setting = False
        elif leave_button.rect.collidepoint(mouse_pos):
            manager.leave_setting = True
            manager.sub_setting = False

def draw_leave_setting(manager):
    mouse_pos = pygame.mouse.get_pos()
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    leave_setting_width = 300
    leave_setting_height = 278.75
    leave_setting_rect = pygame.Rect(0,0,leave_setting_width,leave_setting_height)
    leave_setting_rect.center = (SCREEN_WIDTH // 2, 450)
    pygame.draw.rect(screen, (10, 20, 30), leave_setting_rect, border_radius= 15)
    if leave_setting_rect.collidepoint(mouse_pos):
        color_border = NEON_GREEN
    else:
        color_border = GREY
    pygame.draw.rect(screen, color_border, leave_setting_rect, 3, border_radius= 15)

    button_width = 200
    button_height = 85
    leave2mainmenu_button = button.TextButton(SCREEN_WIDTH // 2 - button_width /2, 389 - button_height / 2, button_width, button_height,"Main Menu", font32, manager.sfx)
    leave2desktop_button = button.TextButton(SCREEN_WIDTH // 2 - button_width /2, 511 - button_height / 2, button_width, button_height,"Desktop", font32, manager.sfx)
    leave2mainmenu_button.draw(screen)
    leave2desktop_button.draw(screen)

    mouse_pos = pygame.mouse.get_pos()
    if pygame.mouse.get_just_released()[0]:
        if leave2mainmenu_button.rect.collidepoint(mouse_pos):
            #Lưu game chơi dở
            if not manager.game.lose:
                manager.data_manager.current_user.is_playing_unfinished = True
                manager.data_manager.current_user.save_unfinished_game(manager)
                manager.data_manager.save_data()
                manager.data_manager.load_data()
            manager.state = "Main Menu"
            manager.setting = False
            manager.sub_setting = False
            manager.leave_setting = False
            #Thực hiện lưu game (Làm sau)
            manager.game = None # Nhớ lưu game
        elif leave2desktop_button.rect.collidepoint(mouse_pos):
            #Lưu game chơi dở (nếu có)
            active_list = manager.data_manager.get_active_list()
            if manager.state == "Game Play" and not manager.game.lose:
                    manager.data_manager.current_user.is_playing_unfinished = True
                    
            if manager.data_manager.current_user:
                    if manager.data_manager.current_user.is_playing_unfinished:
                        if len(active_list) < 5:
                            if manager.state == "Game Play" and not manager.game.lose:
                                manager.data_manager.current_user.save_unfinished_game(manager)
                            manager.data_manager.save_data()
                            pygame.quit()
                            sys.exit()
                        else:
                            manager.overwrite_noti = True
                    else:
                        manager.data_manager.save_data()
                        pygame.quit()
                        sys.exit()
            else:
                manager.data_manager.save_data()
                pygame.quit()
                sys.exit()

def draw_setting(manager):
    mouse_pos = pygame.mouse.get_pos()
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    setting_w = 600
    setting_h = 800
    setting_x = (SCREEN_WIDTH - setting_w) // 2
    setting_y = (SCREEN_HEIGHT - setting_h) // 2
    panel_rect = pygame.Rect(setting_x, setting_y, setting_w, setting_h)

    #Vẽ nền, viền
    pygame.draw.rect(screen, DARK_BG, panel_rect, border_radius=15)
    pygame.draw.rect(screen, NEON_GREEN, panel_rect, 3, border_radius=15) 
    # Tiêu đề Cài đặt
    title_surf = font40.render("Cài đặt", True, WHITE)
    screen.blit(title_surf, (setting_x + 40, setting_y + 30))

    # Nút "X" 
    close_size = 40
    close_rect = pygame.Rect(setting_x + setting_w - 55, setting_y + 20, close_size, close_size)
    mouse_pos = pygame.mouse.get_pos()
    if close_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (200, 50, 50), close_rect, border_radius=8) 
    else:
        pygame.draw.rect(screen, (50, 50, 50), close_rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, close_rect, 2, border_radius=8)

    x_surf = font30.render("X", True, WHITE)
    x_text_rect = x_surf.get_rect(center=close_rect.center)
    screen.blit(x_surf, x_text_rect)

    # 5. Phần "Âm thanh"
    header_y = setting_y + 130
    
    header_surf = font30.render("Âm thanh", True, NEON_GREEN)
    screen.blit(header_surf, (setting_x + 50, header_y))

    def draw_checkbox(label, y, is_on):
        label_surf = font30.render(label, True, WHITE)
        screen.blit(label_surf, (setting_x + 80, y))
        
        box_size = 36
        # Canh lề phải cho ô vuông 
        box_x = setting_x + setting_w - 100 
        box_rect = pygame.Rect(box_x, y - 2, box_size, box_size)
        
        if is_on:
            pygame.draw.rect(screen, NEON_GREEN, box_rect, border_radius=6)
            
        else:
            pygame.draw.rect(screen, DARK_BG, box_rect, border_radius=6)
            pygame.draw.rect(screen, (100, 100, 100), box_rect, 2, border_radius=6) 

        return box_rect

    # Vẽ 2 checkbox
    sfx_rect = draw_checkbox("Hiệu ứng", header_y + 60, manager.sfx)
    music_rect = draw_checkbox("Nhạc nền", header_y + 120, manager.background_music)

    # Đường kẻ ngang màu xanh neon phân cách
    line_y = setting_y + setting_h - 60
    pygame.draw.line(screen, NEON_GREEN, (setting_x, line_y), (setting_x + setting_w, line_y), 2)

    # Tên người chơi
    if manager.data_manager.current_user:
        name_surf = font20.render(f"{manager.data_manager.current_user.username}", True, WHITE)
        name_rect = name_surf.get_rect(midright=(setting_x + setting_w - 20, line_y + 30))
        screen.blit(name_surf, name_rect)

    if pygame.mouse.get_just_released()[0]:
        if sfx_rect.collidepoint(mouse_pos):
            manager.sfx = not manager.sfx
        if music_rect.collidepoint(mouse_pos):
            manager.background_music = not manager.background_music
            if not manager.background_music:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()

        if close_rect.collidepoint(mouse_pos):
            manager.setting = False