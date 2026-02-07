import pygame
import sys
import base64
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
def draw_overwrite_noti(screen, manager):
    active_users = manager.data_manager.get_active_list()
    mouse_pos = pygame.mouse.get_pos()
    noti_w, noti_h = 600, 750
    noti_x = (SCREEN_WIDTH - noti_w) // 2
    noti_y = (SCREEN_HEIGHT - noti_h) // 2
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) # Màu đen trong suốt alpha 180
    screen.blit(overlay, (0,0))

    pygame.draw.rect(screen, (30, 30, 30), (noti_x, noti_y, noti_w, noti_h), border_radius=20)
    pygame.draw.rect(screen, (0, 230, 150), (noti_x, noti_y, noti_w, noti_h), 3, border_radius=20)

    title_surf = font40.render("BỘ NHỚ ĐẦY (5/5)!", True, WHITE)
    title_rect = title_surf.get_rect(center=(noti_x + noti_w//2, noti_y + 60))
    screen.blit(title_surf, title_rect)

    msg_lines = ["Bạn phải chọn một tài khoản cũ để ghi đè.", "Dữ liệu chơi dở của người đó sẽ bị mất."]
    for i, line in enumerate(msg_lines):
        msg_surf = font28.render(line, True, (200, 200, 200))
        msg_rect = msg_surf.get_rect(center=(noti_x + noti_w//2, noti_y + 120 + i*35))
        screen.blit(msg_surf, msg_rect)


    btn_start_y = noti_y + 200
    btn_h = 70
    btn_gap = 20
    buttons = []

    for i, user in enumerate(active_users):
        btn_y = btn_start_y + i * (btn_h + btn_gap) 
        
        btn_rect = pygame.Rect(noti_x + 50, btn_y, noti_w - 100, btn_h)
        
        # CHIA NÚT THÀNH 2 PHẦN: Ô SỐ, TÊN
        index_w = 60 # Chiều rộng của ô số 
        
        index_rect = pygame.Rect(btn_rect.x, btn_rect.y, index_w, btn_h)
        
        name_rect = pygame.Rect(btn_rect.x + index_w, btn_rect.y, btn_rect.width - index_w, btn_h)

        # Hover
        if btn_rect.collidepoint(mouse_pos):
            current_name_bg = (50, 50, 50)
        else:
            current_name_bg = (30, 30, 30)
        # Vẽ Ô Số
        pygame.draw.rect(screen, (0, 230, 150), index_rect, border_top_left_radius=10, border_bottom_left_radius=10)
        pygame.draw.rect(screen, BLACK, index_rect, 2, border_top_left_radius=10, border_bottom_left_radius=10) # Viền đen
        
        # Vẽ ô TÊN 
        pygame.draw.rect(screen, current_name_bg, name_rect, border_top_right_radius=10, border_bottom_right_radius=10)
        pygame.draw.rect(screen, (0, 230, 150), name_rect, 2, border_top_right_radius=10, border_bottom_right_radius=10) # Viền đen

        # VẼ CHỮ 
        # Số thứ tự 
        number_surf = font28.render(f"{i+1}", True, BLACK) 
        number_rect = number_surf.get_rect(center=index_rect.center)
        screen.blit(number_surf, number_rect)

        # Tên User
        text_surf = font28.render(f"{user.username}", True, WHITE)
        text_rect = text_surf.get_rect(midleft=(name_rect.x + 20, name_rect.centery)) 
        screen.blit(text_surf, text_rect)

        # Lưu lại btn_rect lớn để xử lý click
        buttons.append((btn_rect, user))

    cancel_rect = pygame.Rect(noti_x + 150, noti_y + noti_h - 100, noti_w - 300, 60)

    # Nút hủy bỏ
    if cancel_rect.collidepoint(mouse_pos):
        cancel_border = (255, 50, 50) 
        cancel_text_color = (255, 50, 50)
    else:
        cancel_border = (0, 230, 150)
        cancel_text_color = WHITE

    close_btn_size = 30
    close_btn_rect = pygame.Rect(noti_x + noti_w - close_btn_size - 20, noti_y + 20, close_btn_size, close_btn_size)
    
    # Nút X
    close_color = WHITE
    if close_btn_rect.collidepoint(mouse_pos):
        close_color = (255, 50, 50)
    pygame.draw.rect(screen, close_color, close_btn_rect, border_radius=5)
    
    # Vẽ chữ X
    x_surf = font30.render("X", True, WHITE if close_btn_rect.collidepoint(mouse_pos) else BLACK)
    x_rect = x_surf.get_rect(center=close_btn_rect.center)
    screen.blit(x_surf, x_rect)

    pygame.draw.rect(screen, (30, 30, 30), cancel_rect, border_radius=15)
    pygame.draw.rect(screen, cancel_border, cancel_rect, 3, border_radius=15)

    cancel_surf = font26.render("HỦY BỎ", True, cancel_text_color)
    cancel_text_rect = cancel_surf.get_rect(center=cancel_rect.center)
    screen.blit(cancel_surf, cancel_text_rect)

    # Xử lý click

    mouse_pos = pygame.mouse.get_pos()
    if pygame.mouse.get_just_released()[0]:
        if close_btn_rect.collidepoint(mouse_pos):
            manager.overwrite_noti = False
        if cancel_rect.collidepoint(mouse_pos):
            manager.data_manager.current_user.is_playing_unfinished = False
            manager.data_manager.save_data()
            manager.overwrite_noti = False

        for btn_rect, user in buttons:
            if btn_rect.collidepoint(mouse_pos):
                user.is_playing_unfinished = False
                if manager.data_manager.current_user:
                    if user.username != manager.data_manager.current_user.username:
                        if manager.game:
                            manager.data_manager.current_user.save_unfinished_game(manager)
                manager.data_manager.save_data()
                manager.overwrite_noti = False
