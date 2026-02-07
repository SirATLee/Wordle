import pygame
import random
import time
import game_mechanism
import button
import base64
from overwriteUI import *
from setting import *
from assets import *
from mode_choosing import no_lives_popup, draw_no_lives_pop_up
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Wordle")
font = pygame.font.Font(FONT,55)
large_font = pygame.font.Font(FONT,75)
small_font = pygame.font.Font(FONT,20)
keyboard_img = pygame.image.load("images/button_img/keyboard.png")
keyboard_off_img = pygame.image.load("images/button_img/keyboard_off.png")
undo_img = pygame.image.load("images/button_img/undo.png")
redo_img = pygame.image.load("images/button_img/redo.png")
setting_img = pygame.image.load("images/button_img/setting.png")
hint_img = pygame.image.load("images/button_img/hint.png")
popup_font = pygame.font.Font(FONT,35)
keyboard_font = pygame.font.Font(FONT,35)
special_key_font  = pygame.font.Font(FONT,25) 

switch_sfx = pygame.mixer.Sound("sound/switch.mp3")
switch_sfx.set_volume(0.3)

popup_timer = 0
popup_msg = ""

# Làm thông báo game
def game_notify(manager):
    if manager.game.stop:
        #Thắng
        if not manager.game.lose:
            # noti_surface = font.render(f'Tốt lắm', True, BLACK)
            # noti_rect = noti_surface.get_rect(center = (SCREEN_WIDTH // 2, 50))
            # screen.blit(noti_surface,noti_rect)
            pass
        #Thua
        else:
            manager.data_manager.current_user.is_playing_unfinished = False
            #Tính điểm đạt được
            manager.game.total_score = round(caculate_final_score(manager)//10)
            #Lấy Streak
            streak = len(manager.game.stages_time)
            #Cập nhật thông tin tài khoản
            if not manager.data_manager.current_user.is_updated:
                manager.data_manager.current_user.update_after_game(manager.game.mode, manager.game.total_score, streak, manager.game.type)
                manager.data_manager.save_data()
                manager.data_manager.current_user.is_updated = True
            game_over_notify(manager)

def game_over_notify(manager):
    #Làm tối màn hình
    overlay = pygame.Surface((800, 1000), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200)) # Màu đen trong suốt
    screen.blit(overlay, (0, 0))

    popup_rect = pygame.Rect(150, 150, 500, 550) 
    pygame.draw.rect(screen, (35, 35, 35), popup_rect, border_radius=10)

    border_color = (6, 214, 160)
    pygame.draw.rect(screen, border_color, popup_rect, width=2, border_radius=10)

    title_surf = font.render("Chúc mừng", True, (255, 255, 255))
    screen.blit(title_surf, (popup_rect.centerx - title_surf.get_width()//2, 190))

    score_label = popup_font.render("TỔNG ĐIỂM", True, (180, 180, 180))
    screen.blit(score_label, (popup_rect.centerx - score_label.get_width()//2, 260))

    score_val = large_font.render(str(manager.game.total_score), True, (6, 214, 160))
    screen.blit(score_val, (popup_rect.centerx - score_val.get_width()//2, 300))

    word_label = popup_font.render("ĐÁP ÁN:", True, (180, 180, 180))
    screen.blit(word_label, (popup_rect.centerx - word_label.get_width()//2, 390))
    
    word_val = popup_font.render(manager.game.secret_word.upper(), True, (255, 255, 255))
    screen.blit(word_val, (popup_rect.centerx - word_val.get_width()//2, 440))

    button_width = 200
    button_height = 100
    button_margin = (500 - 2*button_width)/3
    main_menu_button = button.TextButton(150 + button_margin ,600 - button_height / 2, button_width, button_height,"Trang Chủ", font32, manager.sfx)
    play_again_button = button.TextButton(150 + 2*button_margin + button_width,600 - button_height / 2, button_width, button_height,"Thử lại", font32, manager.sfx)
    main_menu_button.draw(screen)
    play_again_button.draw(screen)

    mouse_pos = pygame.mouse.get_pos()
    if pygame.mouse.get_just_released()[0]:
        if main_menu_button.rect.collidepoint(mouse_pos):
            manager.game = None
            manager.state = "Main Menu"
            manager.data_manager.save_data()
        elif play_again_button.rect.collidepoint(mouse_pos):
            type = manager.game.type
            if type == "PRACTICE":
                manager.game = game_mechanism.Game(manager.game.word_len,manager.game.mode)
                manager.data_manager.current_user.is_updated = False
                print(manager.game.secret_word,1)
                manager.state = "Game Play"
                manager.data_manager.save_data()
            else:
                if manager.data_manager.current_user.ranked_lives > 0:
                    manager.data_manager.current_user.ranked_lives -= 1

                    if manager.data_manager.current_user.ranked_lives == 2:
                        manager.data_manager.current_user.last_life_regen = time.time()

                    manager.game = game_mechanism.Game(manager.game.word_len,manager.game.mode)
                    manager.game.type = "RANK"
                    manager.data_manager.current_user.is_updated = False
                    print(manager.game.secret_word,1)
                    manager.state = "Game Play"
                    manager.data_manager.save_data()
                else:
                    no_lives_popup(manager)
#Làm màn hình dừng
def display_current_score(game):
    score_surface = font.render(f'{round(game.total_score/10)}', True, BLACK)
    score_rect = score_surface.get_rect(center = (SCREEN_WIDTH // 2, 50))
    screen.blit(score_surface,score_rect)

def display_current_mode(game):
    text_surf = font20.render(f"Mode: {game.mode}", True, (0, 0, 0)) # Chữ màu Đen
    
    padding_x = 12 
    padding_y = 6 
    box_w = text_surf.get_width() + padding_x * 2
    box_h = text_surf.get_height() + padding_y * 2
    
    box_rect = pygame.Rect(SCREEN_WIDTH - box_w - 20 , 85, box_w, box_h)
    pygame.draw.rect(screen, (255, 255, 255), box_rect, border_radius=8)
    pygame.draw.rect(screen, (0, 0, 0), box_rect, 2, border_radius=8)
    text_rect = text_surf.get_rect(center=box_rect.center)
    screen.blit(text_surf, text_rect)

#Làm thông báo popup
def not_valid_popup(manager):
    global popup_timer, popup_msg
    popup_timer = pygame.time.get_ticks() + 1500
    if manager.game.mode == "VI" or manager.game.mode == "EN":
        popup_msg = "Từ không hợp lệ"
    else:
        popup_msg = "Biểu thức không hợp lệ"

def too_short_popup(manager):
    global popup_timer, popup_msg
    popup_timer = pygame.time.get_ticks() + 1500
    if manager.game.mode == "VI" or manager.game.mode == "EN":
        popup_msg = "Từ quá ngắn"
    else:
        popup_msg = "Biểu thức không đủ dài"

def draw_pop_up():
    if pygame.time.get_ticks() < popup_timer:
        text_surf = popup_font.render(popup_msg, True, (255,255,255,70))
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        
        bg_rect = text_rect.inflate(20, 15)
        pygame.draw.rect(screen, (40, 40, 40, 70), bg_rect, border_radius=5)
        screen.blit(text_surf, text_rect)

#Gợi ý cấu trúc cho mode tiếng việt
def get_structure_hint(manager):
    list = manager.game.secret_word_with_space.split(" ")
    num_of_syl = len(list)

    syl_hint = f'Từ này có {num_of_syl} âm tiết'
    detail_hint = ""

    if num_of_syl > 1:
        thutu = ['đầu tiên', 'thứ hai', 'thứ ba', 'thứ tư']
        for i in range(num_of_syl):
            detail_hint += f', từ {thutu[i]} có {len(list[i])} chữ'
            if i == 1 and num_of_syl > 2:
                detail_hint += "\n"
    return syl_hint + detail_hint + "."
def structure_hint_box(manager):
    if manager.game.mode == "VI" and manager.game.hint:
        hint = get_structure_hint(manager)
        box_width = 600
        box_height = 100
        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = 130

        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(screen, (25, 65, 65), box_rect, border_radius=15)

        pygame.draw.rect(screen, (30, 100, 100), box_rect, width=2, border_radius=15)

        hint_surface = small_font.render(f"Gợi ý cấu trúc:", True, WHITE)
        hint_rect = hint_surface.get_rect(center = (400, box_y +20))
        screen.blit(hint_surface, hint_rect)
        
        detail_surface = small_font.render(hint, True, (0, 255, 200)) 

        detail_rect = detail_surface.get_rect(center=(400, box_y + 60))
        screen.blit(detail_surface, detail_rect)
def draw_hint_button(manager):
    if manager.game.mode == "VI":
        hint_button = button.ImgButton(675,50,hint_img,50,50, False)
        hint_button.draw_button()

        mouse_pos = pygame.mouse.get_pos()
        if hint_button.rect.collidepoint(mouse_pos) and pygame.mouse.get_just_released()[0]:
            manager.game.hint = not manager.game.hint
            if manager.sfx:
                switch_sfx.play()

#Tạo nút bật/tắt setting
def draw_setting_button(manager):
    setting_button = button.ImgButton(750,50,setting_img,50,50, False)
    setting_button.draw_button()

    mouse_pos = pygame.mouse.get_pos()
    if setting_button.rect.collidepoint(mouse_pos) and pygame.mouse.get_just_released()[0]:
            if manager.setting or manager.sub_setting or manager.leave_setting:
                manager.setting = False
                manager.sub_setting = False
                manager.leave_setting = False
            else:
                manager.sub_setting = True

def unredo_button(manager):
    button_size = 50

    if manager.game.keyboard_switch:
        undo_button = button.ImgButton(65, start_y - button_size,undo_img,button_size,button_size, False)
        redo_button = button.ImgButton(65 + button_size + 15, start_y - button_size,redo_img,button_size,button_size, False)
    else:
        undo_button = button.ImgButton(65, SCREEN_HEIGHT - button_size,undo_img,button_size,button_size, False)
        redo_button = button.ImgButton(65 + button_size + 15, SCREEN_HEIGHT - button_size,redo_img,button_size,button_size, False)
    undo_button.draw_button()
    redo_button.draw_button()
    pygame.draw.rect(screen, BLACK, undo_button.rect, 3, border_radius= 10)
    pygame.draw.rect(screen, BLACK, redo_button.rect, 3, border_radius= 10)
    mouse_pos = pygame.mouse.get_pos()
    if not manager.setting and not manager.sub_setting and not manager.leave_setting:
        if undo_button.rect.collidepoint(mouse_pos) and pygame.mouse.get_just_released()[0] and not manager.game.lose:
            manager.game.undo()
            if manager.sfx:
                switch_sfx.play()
        elif redo_button.rect.collidepoint(mouse_pos) and pygame.mouse.get_just_released()[0] and not manager.game.lose:
            manager.game.redo()
            if manager.sfx:
                switch_sfx.play()
            
def display_remaining_undo(manager):
    pause_surface = special_key_font.render(f'Lượt quay lại: {manager.game.remaining_undo}', True, BLACK)
    pause_rect = pause_surface.get_rect(topleft = (25, 85))
    screen.blit(pause_surface,pause_rect)
def no_undo_remaining_popup():
    global popup_timer, popup_msg
    popup_timer = pygame.time.get_ticks() + 1500
    popup_msg = "Bạn đã hết lượt Quay Lại"
#Tạo nút bật/tắt bàn phím 
def keyboard_switch_button(manager):
    if manager.game.keyboard_switch:
        kb_button = button.ImgButton(50,50,keyboard_img,50,50, False)
    else:
        kb_button = button.ImgButton(50,50,keyboard_off_img,50,50, False)
    
    kb_button.draw_button()

    mouse_pos = pygame.mouse.get_pos()
    if not manager.setting and not manager.sub_setting and not manager.leave_setting:
        if kb_button.rect.collidepoint(mouse_pos) and pygame.mouse.get_just_released()[0] and not manager.game.lose:
            manager.game.keyboard_switch = not manager.game.keyboard_switch
            if manager.sfx:
                switch_sfx.play()

#Làm bàn phím
def draw_keyboard(manager):
    global start_y
    backspace_img = pygame.image.load("images/backspace.png").convert_alpha()
    game = manager.game
    #Bàn phím Latinh
    mouse_pos = pygame.mouse.get_pos()
    if game.mode == "EN" or game.mode == "VI":
        start_y = 700
        for row in range(3):
            number_of_keys = len(game.keyboard[row])
            if row != 2:
                total_width = number_of_keys * (KEYBOARD_TILE_WIDTH + MARGIN) - MARGIN
            else:
                total_width = number_of_keys * (KEYBOARD_TILE_WIDTH + MARGIN) - MARGIN + 1.5 *KEYBOARD_TILE_WIDTH
            start_x = (SCREEN_WIDTH - total_width) // 2
            for col in range(number_of_keys):
                if row == 2:
                    if col != 0:
                        x  = start_x + col*(KEYBOARD_TILE_WIDTH + MARGIN) + 0.75 * KEYBOARD_TILE_WIDTH
                    else:
                        x = start_x
                else:
                    x = start_x + col*(KEYBOARD_TILE_WIDTH + MARGIN)
                y = start_y + row*(KEYBOARD_TILE_HEIGHT + MARGIN)

                #Chỉnh màu ký tự
                if game.keyboard[row][col][1] == "GREY":
                    key_bg_color, key_text_color = GREY, WHITE
                elif game.keyboard[row][col][1] == "YELLOW":
                    key_bg_color, key_text_color = YELLOW, WHITE
                elif game.keyboard[row][col][1] == "GREEN":
                    key_bg_color, key_text_color= GREEN, WHITE
                else:
                    key_bg_color, key_text_color= WHITE, BLACK


                #Vẽ bàn phím

                if game.keyboard[row][col][0] != "ENTER" and game.keyboard[row][col][0] != "BACKSPACE":
                    key_width = KEYBOARD_TILE_WIDTH
                    key_font = keyboard_font
                else:
                    key_width = 1.75 * KEYBOARD_TILE_WIDTH
                    key_font = special_key_font

                key_rect = pygame.Rect(x, y, key_width, KEYBOARD_TILE_HEIGHT)
                pygame.draw.rect(screen, key_bg_color, key_rect, border_radius=10)

                #Thêm viền cho các phím màu trằng
                if key_bg_color == WHITE:
                    pygame.draw.rect(screen, OUTLINE, (x, y, key_width, KEYBOARD_TILE_HEIGHT), 3, border_radius=10)

                if game.keyboard[row][col][0] != "BACKSPACE":
                    char_surface = key_font.render(game.keyboard[row][col][0], True, key_text_color)
                else:
                    char_surface = pygame.transform.scale(backspace_img, (45, 45))
                char_rect = char_surface.get_rect(center=(x + key_width // 2, y + KEYBOARD_TILE_HEIGHT // 2))
                screen.blit(char_surface, char_rect)

                #Tương tác bàn phím với chuột
                if not manager.sub_setting and not manager.leave_setting and not manager.setting and not manager.game.lose and not manager.overwrite_noti:
                    if key_rect.collidepoint(mouse_pos):
                        #Giảm opacity khi hover
                        hover_surf = pygame.Surface((key_width, KEYBOARD_TILE_HEIGHT), pygame.SRCALPHA)
                        pygame.draw.rect(hover_surf, (255, 255, 255, 70), (0, 0, key_width, KEYBOARD_TILE_HEIGHT), border_radius=10)
                        screen.blit(hover_surf, (x, y))

                        #Dùng bàn phím ảo bằng chuột
                        if pygame.mouse.get_just_pressed()[0]:
                            if game.stop:
                                word_len = random.randint(5,6)
                                manager.game = game_mechanism.Game(word_len)
                                game = manager.game
                                print(manager.game.secret_word)
                            else:
                                if game.keyboard[row][col][0] == "ENTER":
                                    if game.current_col == game.word_len:
                                        if game.is_valid():
                                            game.check_guess()
                                        else: not_valid_popup(manager)
                                    else: too_short_popup(manager)
                                elif game.keyboard[row][col][0] == "BACKSPACE":
                                    if game.current_col > 0:
                                        game.guess_undo_stack[game.current_row].append(game.current_guesses)
                                        game.guesses[game.current_row][game.current_col - 1] = ""
                                        game.current_guesses = game.current_guesses[:-1]
                                        game.current_col -= 1
                                else:
                                    if game.current_col < game.word_len:
                                        game.guess_undo_stack[game.current_row].append(game.current_guesses)
                                        game.guesses[game.current_row][game.current_col]  = game.keyboard[row][col][0]
                                        game.current_guesses += game.keyboard[row][col][0]
                                        game.current_col += 1

    #Bàn phím biểu thức
    else:
        start_y = 700 + (game.word_len - 2 - 6)*(TILE_SIZE + MARGIN)
        total_width = 10 * (KEYBOARD_TILE_WIDTH + MARGIN) - MARGIN
        start_x = (SCREEN_WIDTH - total_width) // 2
        for row in range(2):
            number_of_keys = len(game.keyboard[row])
            for col in range(number_of_keys):
                y = start_y + row*(KEYBOARD_TILE_HEIGHT + MARGIN)
                if row == 0:
                    x = start_x + col*(KEYBOARD_TILE_WIDTH + MARGIN)
                else:
                    if col == 6:
                        x  = start_x + (col + 2)*(KEYBOARD_TILE_WIDTH + MARGIN)
                    else:
                        x = start_x + col*(KEYBOARD_TILE_WIDTH + MARGIN)
                #Chỉnh màu ký tự
                if game.keyboard[row][col][1] == "GREY":
                    key_bg_color, key_text_color = GREY, WHITE
                elif game.keyboard[row][col][1] == "YELLOW":
                    key_bg_color, key_text_color = YELLOW, WHITE
                elif game.keyboard[row][col][1] == "GREEN":
                    key_bg_color, key_text_color= GREEN, WHITE
                else:
                    key_bg_color, key_text_color= WHITE, BLACK

                #Vẽ bàn phím

                if game.keyboard[row][col][0] != "ENTER" and game.keyboard[row][col][0] != "BACKSPACE":
                    key_width = KEYBOARD_TILE_WIDTH
                    key_font = keyboard_font
                else:
                    if game.keyboard[row][col][0] == "ENTER":
                        key_width = 3 * KEYBOARD_TILE_WIDTH + 2 * MARGIN
                        key_font = special_key_font
                    else:
                        key_width = 2 * KEYBOARD_TILE_WIDTH + MARGIN
                        key_font = special_key_font

                key_rect = pygame.Rect(x, y, key_width, KEYBOARD_TILE_HEIGHT)
                pygame.draw.rect(screen, key_bg_color, key_rect, border_radius=10)


                #Thêm viền cho các phím màu trằng
                if key_bg_color == WHITE:
                    pygame.draw.rect(screen, OUTLINE, (x, y, key_width, KEYBOARD_TILE_HEIGHT), 3, border_radius=10)

                if game.keyboard[row][col][0] != "BACKSPACE":
                    char_surface = key_font.render(game.keyboard[row][col][0], True, key_text_color)
                else:
                    char_surface = pygame.transform.scale(backspace_img, (45, 45))
                char_rect = char_surface.get_rect(center=(x + key_width // 2, y + KEYBOARD_TILE_HEIGHT // 2))
                screen.blit(char_surface, char_rect)

                if not manager.sub_setting and not manager.leave_setting and not manager.setting and not manager.game.lose and not manager.overwrite_noti:
                    if key_rect.collidepoint(mouse_pos):
                        #Giảm opacity khi hover
                        hover_surf = pygame.Surface((key_width, KEYBOARD_TILE_HEIGHT), pygame.SRCALPHA)
                        pygame.draw.rect(hover_surf, (255, 255, 255, 70), (0, 0, key_width, KEYBOARD_TILE_HEIGHT), border_radius=10)
                        screen.blit(hover_surf, (x, y))

                        #Dùng bàn phím ảo bằng chuột
                        if pygame.mouse.get_just_pressed()[0]:
                            if game.stop:
                                word_len = game.word_len
                                mode = game.mode
                                manager.game = game_mechanism.Game(word_len,mode)
                                game = manager.game
                                print(manager.game.secret_word)
                            else:
                                if game.keyboard[row][col][0] == "ENTER":
                                    if game.current_col == game.word_len:
                                        if game.is_valid():
                                            game.check_guess()
                                        else: not_valid_popup(manager)
                                    else: too_short_popup(manager)
                                elif game.keyboard[row][col][0] == "BACKSPACE":
                                    if game.current_col > 0:
                                        game.guess_undo_stack[game.current_row].append(game.current_guesses)
                                        game.guesses[game.current_row][game.current_col - 1] = ""
                                        game.current_guesses = game.current_guesses[:-1]
                                        game.current_col -= 1
                                else:
                                    if game.current_col < game.word_len:
                                        game.guess_undo_stack[game.current_row].append(game.current_guesses)
                                        game.guesses[game.current_row][game.current_col]  = game.keyboard[row][col][0]
                                        game.current_guesses += game.keyboard[row][col][0]
                                        game.current_col += 1
#Vẽ lưới, tô màu các ô
def draw_grid(game):
    total_width = game.word_len * (TILE_SIZE + MARGIN) - MARGIN
    start_x = (SCREEN_WIDTH - total_width) // 2
    start_y = 125 
    for row in range(game.guess_attempts):
            for col in range(game.word_len):
                x = start_x + col*(TILE_SIZE + MARGIN)
                y = start_y + row*(TILE_SIZE + MARGIN)

                bg_color = WHITE
                text_color = BLACK

                if row < game.current_row:
                    if game.letter_color[row][col] == "GREY": bg_color = GREY
                    elif game.letter_color[row][col] == "YELLOW": bg_color = YELLOW
                    elif game.letter_color[row][col] == "GREEN": bg_color = GREEN
                    text_color = WHITE

                

                pygame.draw.rect(screen, bg_color, (x, y, TILE_SIZE, TILE_SIZE))
                if bg_color == WHITE:
                    pygame.draw.rect(screen, OUTLINE, (x, y, TILE_SIZE, TILE_SIZE), 3)
                if row == game.current_row and col == game.current_col:
                    pygame.draw.rect(screen, RED, (x, y, TILE_SIZE, TILE_SIZE), 3)

                if game.guesses[row][col]:
                    char_suface = font.render(game.guesses[row][col], True, text_color)
                    char_rect = char_suface.get_rect(center = (x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                    screen.blit(char_suface,char_rect)

def get_remaining_time(manager):
    game = manager.game
    if not manager.game.stop:
        current_time = pygame.time.get_ticks()
        game.total_time_remain = game.total_time - (current_time - game.game_start_time) + game.time_added
        if game.total_time_remain > game.total_time:
            game.time_added = (current_time - game.game_start_time)
    return max(0,game.total_time_remain // 1000)
def draw_timer_bar(manager, screen):
    remaining_seconds = get_remaining_time(manager)
    if remaining_seconds == 0:
        manager.game.stop = True
        manager.game.lose = True
        return
    
    full_bar_width = SCREEN_WIDTH
    bar_width = (remaining_seconds / 180) * full_bar_width
    bar_rect = pygame.Rect(0, 0, bar_width, 10)
    
    
    # Xanh nếu > 30s, Đỏ nếu < 30s
    color = GREEN if remaining_seconds > 30 else RED
    pygame.draw.rect(screen, color, bar_rect, border_radius=3)

def caculate_final_score(manager):
    total_score = 0
    base_score = 1000
    for i in range(len(manager.game.stages_time)):
        stage_time = manager.game.stages_time[i] / 1000
        
        speed_bonus = max(0,90 - stage_time)*(10 + i)
        stage_score = (base_score + speed_bonus)*(1 + i*0.2)

        total_score += stage_score
    
    green = 0
    yellow = 0
    grey = 0
    for row in manager.game.keyboard:
        for key in row:
            if key[1] == "GREEN": green += 1
            elif key[1] == "YELLOW": yellow += 1
            elif key[1] == "GREY": grey += 1
    loss_score = (50*green + 30*yellow + 10*grey)*(1 + (len(manager.game.stages_time)+1)*0.2)

    return total_score + loss_score


#Gameplay tổng thể
def draw_gameplay(manager):
    draw_grid(manager.game)

    #Bàn phím
    keyboard_switch_button(manager)
    if manager.game.keyboard_switch:
        draw_keyboard(manager)
    #Hiển thị điểm hiện tại
    display_current_score(manager.game)
    #Hiển thị mode
    display_current_mode(manager.game)
    #Gợi ý cấu trúc cho mode VI
    draw_hint_button(manager)
    structure_hint_box(manager)
    #Undo Redo
    display_remaining_undo(manager)
    unredo_button(manager)
    
    #Thanh căn thời gian
    draw_timer_bar(manager,screen)
    #Các loại thông báo
    game_notify(manager)
    draw_pop_up()
    draw_no_lives_pop_up()
    #Setting
    draw_setting_button(manager)
    if manager.sub_setting:
        draw_sub_setting(manager)
    if manager.leave_setting:
        draw_leave_setting(manager)
    if manager.setting:
        draw_setting(manager)
    if manager.overwrite_noti:
        draw_overwrite_noti(screen, manager)