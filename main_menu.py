import pygame
import button
import time
import base64
from overwriteUI import *
from game_mechanism import *
from login_popup import *
from logout_popup import *
from setting import *
from assets import *
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
font90 = pygame.font.Font(FONT,100)
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Wordle")
font = pygame.font.Font(FONT,75)
font_user = pygame.font.Font(FONT,20)
playbut_img = pygame.image.load("images/button_img/test_button.png")
user_account_img = pygame.image.load("images/button_img/user_account.png")
logout_img = pygame.image.load("images/button_img/logout.png")
setting_img = pygame.image.load("images/button_img/setting.png")
playnow_img = pygame.image.load("images/button_img/choi_ngay.png")
bxh_img = pygame.image.load("images/button_img/bxh.png")
background = pygame.image.load("images/button_img/background.png")
switch_sfx = pygame.mixer.Sound("sound/switch.mp3")
switch_sfx.set_volume(0.3)

background_surface = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_state_changing_button(manager):
    play_button = button.ImgButton(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 75, playnow_img, 282, 120, manager.sfx)
    play_button.draw_button()

    top20_button = button.ImgButton(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 75, bxh_img, 282, 120, manager.sfx)
    top20_button.draw_button()

    mouse_pos = pygame.mouse.get_pos()
    if pygame.mouse.get_just_released()[0] and manager.popup is None and manager.logout_popup is None and not manager.setting and not manager.user_info and not manager.overwrite_noti and not manager.continue_popup:
        if play_button.rect.collidepoint(mouse_pos):
            if manager.data_manager.current_user is not None:
                print(manager.data_manager.current_user.is_playing_unfinished)
                if manager.data_manager.current_user.is_playing_unfinished == False:
                    manager.state = "Mode Choosing"
                else:
                    manager.continue_popup = True
            else:
                manager.popup = LoginPopup(SCREEN_WIDTH, SCREEN_HEIGHT, manager)
        elif top20_button.rect.collidepoint(mouse_pos):
            manager.state = "Top-20 List"

def main_menu_title(manager):
    word = "WORDLE"
    color_cycle = [GREEN, YELLOW, GREY ]
    total_width, total_height = font.size(word)
    target_y = 200
    start_x = (SCREEN_WIDTH // 2) - (total_width // 2) - 50
    start_y = target_y - (total_height // 2)
    current_x_pos = start_x
    shadow_offset_x = 5
    shadow_offset_y = 5

    for index, letter in enumerate(word):
        shadow_surface = font90.render(letter, True, BLACK)
        shadow_rect = shadow_surface.get_rect(topleft=(current_x_pos + shadow_offset_x, start_y + shadow_offset_y))
        screen.blit(shadow_surface, shadow_rect)

        current_color = color_cycle[index % len(color_cycle)]

        letter_surface = font90.render(letter, True, current_color)
        letter_rect = letter_surface.get_rect(topleft=(current_x_pos, start_y))
        screen.blit(letter_surface, letter_rect)
        letter_width = font90.size(letter)[0]
        current_x_pos += letter_width - 3

    sub_title_surface = font24.render(f"Premium Edition", True, BLACK)
    sub_title_rect = sub_title_surface.get_rect(center = ((SCREEN_WIDTH // 2 + 140), 280))
    screen.blit(sub_title_surface,sub_title_rect)

    
def draw_setting_button(manager):
    setting_button = button.ImgButton(750,50,setting_img,50,50, False)
    setting_button.draw_button()

    mouse_pos = pygame.mouse.get_pos()
    if setting_button.rect.collidepoint(mouse_pos) and pygame.mouse.get_just_released()[0] and manager.popup is None and manager.logout_popup is None:
            if manager.setting or manager.sub_setting or manager.leave_setting:
                manager.setting = False
                manager.sub_setting = False
                manager.leave_setting = False
            else:
                manager.setting = True
def logout_button(screen, manager):
    logout_button = button.ImgButton(750,950,logout_img,50,50, manager.sfx)
    logout_button.draw_button()

    mouse_pos = pygame.mouse.get_pos()
    if logout_button.rect.collidepoint(mouse_pos) and pygame.mouse.get_just_released()[0] and manager.popup is None and not manager.setting and not manager.continue_popup:
            active_list = manager.data_manager.get_active_list()
            if manager.data_manager.current_user:
                    if manager.data_manager.current_user.is_playing_unfinished:
                        if len(active_list) < 5:
                            manager.data_manager.save_data()
                            manager.logout_popup = LogoutPopup(SCREEN_WIDTH,SCREEN_HEIGHT,manager)
                        else:
                            manager.overwrite_noti = True
                    else:
                        manager.data_manager.save_data()
                        manager.logout_popup = LogoutPopup(SCREEN_WIDTH,SCREEN_HEIGHT,manager)
def draw_practice_switch(screen, x, y, manager):
    user = manager.data_manager.current_user
    practice_surface = font22.render(f'Luyện tập', True, BLACK)
    practice_rect = practice_surface.get_rect(topleft = (x - 105,y + 4))
    screen.blit(practice_surface,practice_rect)

    # Vẽ khung chứa
    width, height = 80, 38
    rect = pygame.Rect(x, y, width, height)
    # Màu nền: Xanh lá nếu Practice, Đỏ nếu Ranked (Giới hạn)
    bg_color = (100, 255, 100) if user.is_practice_mode else (255, 100, 100)
    pygame.draw.rect(screen, bg_color, rect, border_radius=25)
    pygame.draw.rect(screen, (0,0,0), rect, 2, border_radius=25)
    
    # Vẽ nút tròn (Switch)
    circle_radius = 15
    if user.is_practice_mode:
        circle_x = x + width - circle_radius - 5 # Gạt sang phải
        status_text = "ON"
    else:
        circle_x = x + circle_radius + 5 # Gạt sang trái
        status_text = "OFF"
        
    pygame.draw.circle(screen, (255, 255, 255), (circle_x, y + height//2), circle_radius)
    pygame.draw.circle(screen, (0,0,0), (circle_x, y + height//2), circle_radius, 2)

    # Vẽ chữ
    font = font20
    text_surf = font.render(status_text, True, (0,0,0))
    if user.is_practice_mode:
        text_rect = text_surf.get_rect(center=(x + width//2 - circle_radius, y + height//2 - 2))
    else:
        text_rect = text_surf.get_rect(center=(x + width//2 + circle_radius, y + height//2 - 2))
        
    screen.blit(text_surf, text_rect)

    if not user.is_practice_mode:
        lives_text = f"Lượt chơi: {user.ranked_lives}/3"
        lives_surf = font.render(lives_text, True, (255, 0, 0))
        screen.blit(lives_surf, (x - 105, y + height + 11))
        if user.ranked_lives < 3:
            remain = 28800 - (time.time() - user.last_life_regen)
            hours = int(remain // 3600)
            mins = int((remain % 3600) // 60)
            time_surf = font18.render(f"+1 in: {hours}h {mins}m", True, BLACK)
            screen.blit(time_surf, (x +20, y + height + 15))

    mouse_pos = pygame.mouse.get_pos()
    if pygame.mouse.get_just_released()[0]:
        if rect.collidepoint(mouse_pos):
            user.is_practice_mode = not user.is_practice_mode
            if manager.sfx:
                switch_sfx.play()
def draw_user_info(screen, manager):
    current_user = manager.data_manager.current_user
    mouse_pos = pygame.mouse.get_pos()
    if current_user is not None:
        name_text = f"Chào, {current_user.username}"
        name_surf = font_user.render(name_text, True, BLACK) 
        box_x = 20
        box_y = 25
        pad_x = 20 
        pad_y = 10

        box_w = name_surf.get_width() + pad_x
        box_h = name_surf.get_height() + pad_y
        
        
        bg_rect = pygame.Rect(box_x, box_y, box_w, box_h)

        pygame.draw.rect(screen, WHITE, bg_rect, border_radius=10) 
    
        pygame.draw.rect(screen, BLACK, bg_rect, width=2, border_radius=10)

        text_rect = name_surf.get_rect(center=bg_rect.center)
        screen.blit(name_surf, text_rect)
        
        info_display_button = button.ImgButton(box_x + box_w + 10 + box_h / 2,42.5,user_account_img, box_h, box_h, False)
        info_display_button.draw_button()

        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_just_released()[0] and manager.popup is None and manager.logout_popup is None and not manager.overwrite_noti and not manager.continue_popup:
            if  info_display_button.rect.collidepoint(mouse_pos):
                manager.user_info = not manager.user_info
    else:
        please_login = TextButton(25, 25, 200, 40, "Vui lòng đăng nhập", font18, False)
        please_login.bg_color = WHITE
        please_login.text_color = BLACK
        please_login.border_color = BLACK
        please_login.hovered_text_color = (0, 188, 186)
        please_login.draw(screen)

        if not manager.setting:
            if pygame.mouse.get_just_released()[0] and please_login.rect.collidepoint(mouse_pos):
                manager.popup = LoginPopup(SCREEN_WIDTH, SCREEN_HEIGHT, manager)

def draw_continue_popup(screen, manager):
    mouse_pos = pygame.mouse.get_pos()

    popup_width, popup_height = 400, 275 
    x = (SCREEN_WIDTH - popup_width) // 2
    y = (SCREEN_HEIGHT - popup_height) // 2 - 20
        
    font = pygame.font.Font(FONT,20)
    font_bold = pygame.font.Font(FONT,22)

    btn_yes = TextButton(x + 35, y + 175, 140, 70, "CÓ", font, manager.sfx)
    btn_no = TextButton(x + 225, y + 175, 140, 70, "KHÔNG", font, manager.sfx)

    # Lớp phủ mờ
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    # Nền Popup
    popup_rect = pygame.Rect((x, y, popup_width, popup_height))
    border_color = (0, 223, 129)
    if not popup_rect.collidepoint(mouse_pos):
        border_color = GREY
    pygame.draw.rect(screen, (10, 20, 30), (x, y, popup_width, popup_height), border_radius=10)
    pygame.draw.rect(screen,border_color , (x, y, popup_width, popup_height), 2, border_radius=10)

    # Text thông báo
    text_surf = font26.render("Có vẻ bạn đang chơi dở", True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(x + popup_width//2, y + 50))
    screen.blit(text_surf, text_rect)
    ask_surf = font45.render("Tiếp tục?", True, (255, 255, 255))
    ask_rect = text_surf.get_rect(center=(x + popup_width//2 + 50, y + 110))
    screen.blit(ask_surf, ask_rect)

    # Vẽ nút
    btn_yes.draw(screen)
    btn_no.draw(screen)

    
    if pygame.mouse.get_just_released()[0]:
        if btn_yes.rect.collidepoint(mouse_pos):
            manager.state = "Game Play"
            manager.game = Game(6, "EN")
            manager.game.load_unfinished_game(manager.data_manager.current_user)
            manager.continue_popup = False
        
        if btn_no.rect.collidepoint(mouse_pos):
            manager.data_manager.current_user.is_playing_unfinished = False
            manager.data_manager.save_data()
            manager.continue_popup = False

        if not popup_rect.collidepoint(mouse_pos):
            manager.continue_popup = False
        

def draw_profile_UI(screen, manager):
    user = manager.data_manager.current_user
    mouse_pos = pygame.mouse.get_pos()
    
    # Kích thước bảng
    profile_w, profile_h = 650, 430
    profile_x = 25
    profile_y = 75

    margin_left = profile_x + 20
    margin_right = profile_x + profile_w - 20
    center_x = profile_x + profile_w // 2

    # Ddóng bảng khi click ra ngoài
    profileUI_rect = pygame.Rect((profile_x, 0, profile_w, profile_h + profile_y))
    if pygame.mouse.get_just_released()[0] and not profileUI_rect.collidepoint(mouse_pos):
        manager.user_info = False

    pygame.draw.rect(screen, (0, 0, 0), (profile_x + 6, profile_y + 6, profile_w, profile_h), border_radius=15)
    pygame.draw.rect(screen, (30, 30, 30), (profile_x, profile_y, profile_w, profile_h), border_radius=15)
    pygame.draw.rect(screen, (0, 230, 150), (profile_x, profile_y, profile_w, profile_h), 3, border_radius=15)

    # TÊN NGƯỜI CHƠI
    name_surf = font40.render(user.username, True, WHITE)
    screen.blit(name_surf, (margin_left, profile_y + 10)) # Giữ nguyên vị trí cũ

    # TÍNH TOÁN LEVEL: Kinh nghiệm để từ lv n -> n + 1: 700 + 300*1.05^n
    #                   => Tổng kinh nghiệm để lên lvl n: 700*n + 300*(1.05^n - 1)/0.05
    total_exp = user.total_exp
    n = 0
    while total_exp >= 700*n + 300*(1.05**n - 1)/0.05:
        n += 1
    cur_level = n - 1

    # Chữ Level 
    lvl_surf = font24.render(f"Level:   {cur_level}", True, WHITE)
    screen.blit(lvl_surf, (margin_left, profile_y + 60))

    # THANH EXP 
    cur_exp = total_exp - (700*(cur_level) + 300*(1.05**cur_level - 1)/0.05)
    max_exp = 700 + 300*1.05**cur_level
    
    bar_x = profile_x + 135
    bar_y = profile_y + 71
    bar_w = profile_w - 230
    bar_h = 10

    # Vẽ nền thanh XP 
    pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h), border_radius=5)
    # Vẽ viền thanh XP 
    pygame.draw.rect(screen, (0, 230, 150), (bar_x, bar_y, bar_w, bar_h), 1, border_radius=5)

    # Vẽ phần XP đã đạt được 
    fill_width = int((cur_exp / max_exp) * bar_w)
    if fill_width > 0:
        pygame.draw.rect(screen, (0, 230, 150), (bar_x, bar_y, fill_width, bar_h), border_radius=5)

    # Số XP nằm giữa thanh 
    exp_text = font20.render(f"{round(cur_exp)} / {round(max_exp)}", True, WHITE)
    exp_rect = exp_text.get_rect(center=(bar_x + bar_w/2, bar_y - 12))
    screen.blit(exp_text, exp_rect)

    # Level tiếp theo (Bên phải thanh, màu trắng)
    next_lvl_surf = font24.render(str(cur_level + 1), True, WHITE)
    screen.blit(next_lvl_surf, (bar_x + bar_w + 20, profile_y + 60))

    # 5. ĐƯỜNG KẺ NGANG (Màu Neon)
    pygame.draw.line(screen, (0, 230, 150), (margin_left, profile_y + 110), (margin_right, profile_y + 110), 2)

    # 6. THỜI GIAN CHƠI (Màu trắng)
    total_time = user.time_spent
    time_str = f"Thời gian chơi: {total_time // 3600}h {(total_time % 3600) // 60}m {total_time % 60}s"
    time_surf = font26.render(time_str, True, WHITE)
    time_rect = time_surf.get_rect(center=(center_x, profile_y + 135))
    screen.blit(time_surf, time_rect)

    # 7. BẢNG THỐNG KÊ (GRID)
    table_start_y = profile_y + 210
    row_gap = 42

    # Tính toán cột
    col_start_x = margin_left + 200
    col_spacing = (margin_right - col_start_x) / 3
    col_x_centers = [
        col_start_x + col_spacing * 0.5,
        col_start_x + col_spacing * 1.5,
        col_start_x + col_spacing * 2.5
    ]

    rows_labels = [
        "Điểm cao nhất", "Điểm trung bình", 
        "Best Streak", "Số ván đã chơi", "Số lần đoán đúng"
    ]
    col_headers = ["EN", "VI", "EQ"]

    # Tiêu đề cột (EN, VI, EQ) - Màu Neon để nổi bật
    for i, header in enumerate(col_headers):
        head_surf = font28.render(header, True, (0, 230, 150)) # <-- Màu NEON
        head_rect = head_surf.get_rect(center=(col_x_centers[i], table_start_y - 30))
        screen.blit(head_surf, head_rect)

    # Các đường kẻ bảng (Màu Neon hoặc Xám nhạt - Chọn Neon cho đồng bộ)
    line_start_y = table_start_y - 40
    line_end_y = table_start_y + len(rows_labels) * row_gap - 20
    
    # Đường dọc (Giữa thông tin và EN)
    pygame.draw.line(screen, (0, 230, 150), (col_start_x, line_start_y), (col_start_x, line_end_y), 2)
    # Đường dọc (Giữa EN và VI)
    pygame.draw.line(screen, (0, 230, 150), (col_start_x + col_spacing, line_start_y), (col_start_x + col_spacing, line_end_y), 2)
    # Đường dọc (Giữa VI và EQ)
    pygame.draw.line(screen, (0, 230, 150), (col_start_x + col_spacing*2, line_start_y), (col_start_x + col_spacing*2, line_end_y), 2)
    # Đường ngang dưới tiêu đề cột
    pygame.draw.line(screen, (0, 230, 150), (margin_left, profile_y + 200), (margin_right, profile_y + 200), 2)

    # Dữ liệu cho từng dòng
    data_sources = [user.stats_en, user.stats_vi, user.stats_eq]

    for r_idx, label in enumerate(rows_labels):
        current_y = table_start_y + r_idx * row_gap
        
        # Tên hàng (Điểm cao nhất...): Màu Trắng
        label_surf = font22.render(label, True, WHITE) # <-- Màu Trắng
        screen.blit(label_surf, (margin_left, current_y))

        # Dữ liệu số (0, 0.0...): Màu Trắng
        for c_idx, stats in enumerate(data_sources):
            value = stats[r_idx]
            if r_idx == 1: # Điểm trung bình (số thực)
                display_str = str(round(value, 1))
            else: # Số nguyên
                display_str = str(int(value))
            
            val_surf = font22.render(display_str, True, WHITE) # <-- Màu Trắng
            val_rect = val_surf.get_rect(center=(col_x_centers[c_idx], current_y + 10))
            screen.blit(val_surf, val_rect)

    

def draw_main_menu(manager):
    screen.blit(background_surface, (0,0))
    draw_state_changing_button(manager)
    logout_button(screen,manager)
    main_menu_title(manager)
    draw_setting_button(manager)
    draw_user_info(screen, manager)
    if manager.data_manager.current_user:
        draw_practice_switch(screen, 128, 74, manager)
    if manager.popup is not None:
        manager.popup.draw(screen)
    if manager.logout_popup is not None:
        manager.logout_popup.draw(screen)
    if manager.user_info:
        draw_profile_UI(screen, manager)
    if manager.continue_popup:
        draw_continue_popup(screen, manager)
    if manager.setting:
        draw_setting(manager)

    if manager.overwrite_noti:
        draw_overwrite_noti(screen, manager)