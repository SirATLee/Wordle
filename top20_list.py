import random
import pygame
import game_mechanism
import button
import base64
from overwriteUI import *
from assets import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Wordle")
font = pygame.font.Font(FONT,55)
playbut_img = pygame.image.load("images/button_img/test_button.png")
back_img = pygame.image.load("images/button_img/left_arrow.png")
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

def back2mainmenu_button(manager):
    cb_button = button.ImgButton(SCREEN_WIDTH-25-60/2,SCREEN_HEIGHT-25-60/2,back_img,60,60, manager.sfx)
    cb_button.draw_button()

    mouse_pos = pygame.mouse.get_pos()
    if cb_button.rect.collidepoint(mouse_pos) and pygame.mouse.get_just_released()[0]:
        manager.state = "Main Menu"
def top20_title(manager):
    title_surface = font.render(f'Bảng xếp hạng', True, BLACK)
    title_rect = title_surface.get_rect(center = (SCREEN_WIDTH // 2, 40))
    screen.blit(title_surface,title_rect)

def draw_leaderboard(screen, manager): #Dựa vào BXH của Clash of Clans
    mouse_pos = pygame.mouse.get_pos()
    valid_en = [u for u in manager.data_manager.users_save_slots if u.stats_en[0] > 0]
    manager.data_manager.top20_en = sorted(valid_en, key=lambda u: u.stats_en[0], reverse=True)[:20]

    valid_vi = [u for u in manager.data_manager.users_save_slots if u.stats_vi[0] > 0]
    manager.data_manager.top20_vi = sorted(valid_vi, key=lambda u: u.stats_vi[0], reverse=True)[:20]
        
    valid_eq = [u for u in manager.data_manager.users_save_slots if u.stats_eq[0] > 0]
    manager.data_manager.top20_eq = sorted(valid_eq, key=lambda u: u.stats_eq[0], reverse=True)[:20]

    current_tab = manager.leaderboard_mode
    
    if current_tab == "EN":
        data_list = manager.data_manager.top20_en
        stats_index = 0
    elif current_tab == "VI":
        data_list = manager.data_manager.top20_vi
        stats_index = 0
    else: # EQ
        data_list = manager.data_manager.top20_eq
        stats_index = 0

    screen_w, screen_h = screen.get_size()
    
    
    # Khung bảng
    panel_w, panel_h = 600, 750
    panel_x = (screen_w - panel_w) // 2
    panel_y = (screen_h - panel_h) // 2

    # Vẽ nền bảng (Màu xám sáng kiểu CoC)
    pygame.draw.rect(screen, COC_BG_PANEL, (panel_x, panel_y, panel_w, panel_h), border_radius=15)
    pygame.draw.rect(screen, (255, 255, 255), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=15)

    # VẼ CÁC NÚT TABS 
    tabs = ["EN", "VI", "EQ"]
    tab_w = 120
    tab_h = 45
    tab_start_y = panel_y - 35 
    
    tab_rects = [] 
    
    for i, mode in enumerate(tabs):
        tab_x = panel_x + 20 + i * (tab_w + 5)
        rect = pygame.Rect(tab_x, tab_start_y, tab_w, tab_h)
        
        if current_tab == mode:
            bg_color = COC_BG_PANEL 
            y_offset = 0            
            text_color = (0, 0, 0)  
            
        elif rect.collidepoint(mouse_pos):
            bg_color = (200, 200, 205) 
            y_offset = 2               
            text_color = (50, 50, 50)  
            
        else:
            bg_color = (160, 160, 160) 
            y_offset = 5             
            text_color = (100, 100, 100) 

        # Vẽ tab
        pygame.draw.rect(screen, bg_color, (rect.x, rect.y + y_offset, rect.width, rect.height), border_top_left_radius=10, border_top_right_radius=10)
        
        # Vẽ chữ trên tab
        font_tab = font26
        text = font_tab.render(mode, True, text_color)
        text_rect = text.get_rect(center=(rect.centerx, rect.centery + y_offset))
        screen.blit(text, text_rect)
        
        tab_rects.append((rect, mode))

    # Tiêu đề các cột
    header_y = panel_y + 30
    font_small = font18
    screen.blit(font_small.render("Hạng", True, (100, 100, 100)), (panel_x + 30, header_y))
    screen.blit(font_small.render("Người chơi", True, (100, 100, 100)), (panel_x + 100, header_y))
    screen.blit(font_small.render("Điểm", True, (100, 100, 100)), (panel_x + 480, header_y))

    # Vẽ danh sách User
    list_start_y = header_y + 30
    item_h = 60  
    gap = 8    
    
    font_name = font24
    font_score = font28
    font_rank = font24

    # Chỉ vẽ tối đa 10 người để vừa khung hình (hoặc bạn có thể làm scroll sau)
    display_limit = 10 
    current_page = manager.leaderboard_page
    items_per_page = 10
    start_index = (current_page - 1) * items_per_page
    end_index = start_index + items_per_page
    page_data = data_list[start_index:end_index]

    for i, user in enumerate(page_data):
        current_y = list_start_y + i * (item_h + gap)
        row_rect = pygame.Rect(panel_x + 20, current_y, panel_w - 40, item_h)
        
        realrank = start_index + i + 1
        # Nếu là bản thân mình -> Viền xanh lá, Nền hơi xanh
        if manager.data_manager.current_user and user.username == manager.data_manager.current_user.username:
            bg_color = (230, 255, 230)
            border_color = (0, 200, 0)
        else:
            bg_color = COC_ROW_BG
            border_color = (200, 200, 200)

        pygame.draw.rect(screen, (180, 180, 180), (row_rect.x, row_rect.y+3, row_rect.width, row_rect.height), border_radius=10)
        pygame.draw.rect(screen, bg_color, row_rect, border_radius=10)
        pygame.draw.rect(screen, border_color, row_rect, 2, border_radius=10)

        # Vẽ Huy hiệu Rank 
        rank_size = 40
        rank_rect = pygame.Rect(row_rect.x + 10, row_rect.centery - rank_size//2, rank_size, rank_size)
        
        # Màu Top 3
        if i == 0 and current_page == 1: rank_bg = COC_YELLOW
        elif i == 1 and current_page == 1: rank_bg = COC_SILVER
        elif i == 2 and current_page == 1: rank_bg = COC_BRONZE
        else: rank_bg = (100, 100, 100) 
        
        # Vẽ hình khiên/vuông bo tròn cho Rank
        pygame.draw.rect(screen, rank_bg, rank_rect, border_radius=8)
        pygame.draw.rect(screen, (255,255,255), rank_rect, 2, border_radius=8) # Viền trắng
        
        # Số Rank
        rank_surf = font_rank.render(str(realrank), True, (50,50,50) if (i < 3 and current_page == 1) else WHITE)
        rank_text_rect = rank_surf.get_rect(center=rank_rect.center)
        screen.blit(rank_surf, rank_text_rect)

        # Tên User
        name_surf = font_name.render(user.username, True, COC_DARK_TEXT)
        screen.blit(name_surf, (row_rect.x + 70, row_rect.centery - 20))
        
        # Subtext Level
        level_surf = pygame.font.Font(None, 20).render(f"Level: {int(user.total_exp // 1000)}", True, (120, 120, 120))
        screen.blit(level_surf, (row_rect.x + 70, row_rect.centery + 12))

        # Điểm số
        score_val = int(user.stats_en[0]) if current_tab == "EN" else (int(user.stats_vi[0]) if current_tab == "VI" else int(user.stats_eq[0]))
        
        score_bg_w = 120
        score_bg_h = 36
        score_bg_rect = pygame.Rect(row_rect.right - score_bg_w - 10, row_rect.centery - score_bg_h//2, score_bg_w, score_bg_h)
        
        # Vẽ khung điểm 
        pygame.draw.rect(screen, (255, 245, 200), score_bg_rect, border_radius=18)
        pygame.draw.rect(screen, (220, 200, 100), score_bg_rect, 2, border_radius=18)
        
        # Icon Cúp 
        pygame.draw.circle(screen, COC_YELLOW, (score_bg_rect.right - 18, score_bg_rect.centery), 12)
        
        # Số điểm
        score_surf = font_score.render(str(score_val), True, (100, 80, 0)) # Chữ màu vàng nâu
        score_text_rect = score_surf.get_rect(midright=(score_bg_rect.right - 35, score_bg_rect.centery))
        screen.blit(score_surf, score_text_rect)

   
    btn_y = panel_y  - 30
    btn_w, btn_h = 100, 45
    mouse_pos = pygame.mouse.get_pos()
    
    change_page_rect = pygame.Rect((panel_x + panel_w - 50 - btn_w, btn_y, btn_w, btn_h))
    if current_page == 1 and len(data_list) > 10:
        button.draw_nav_btn(" > ", panel_x + panel_w - 50 - btn_w, btn_y, btn_w, btn_h, font28)

    elif current_page == 2:
        button.draw_nav_btn(" < ", panel_x + panel_w - 50 - btn_w, btn_y, btn_w, btn_h, font28)

    if pygame.mouse.get_just_released()[0]:
        if change_page_rect is not None and change_page_rect.collidepoint(mouse_pos):
            manager.leaderboard_page = 3 - manager.leaderboard_page
    if pygame.mouse.get_just_released()[0]:
        for rect, mode in tab_rects:
            if rect.collidepoint(mouse_pos):
                manager.leaderboard_mode = mode
                manager.leaderboard_page = 1
            
def draw_top20_list(manager):
    back2mainmenu_button(manager)
    top20_title(manager)
    draw_leaderboard(screen, manager)
    if manager.overwrite_noti:
        draw_overwrite_noti(screen, manager)

    