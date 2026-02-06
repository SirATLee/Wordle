import pygame
from assets import *
from input_box import *
from button import TextButton

class LoginPopup:
    def __init__(self, screen_w, screen_h, manager_ref):
        self.manager = manager_ref # Tham chiếu ngược lại manager để gọi hàm login
        self.width, self.height = 400, 350
        self.x = (screen_w - self.width) // 2
        self.y = (screen_h - self.height) // 2
        self.rect = pygame.Rect((self.x, self.y, self.width, self.height))

        # Font chữ
        self.font = pygame.font.Font(FONT,24)
        self.font_small = pygame.font.Font(FONT,20)

        # Các thành phần UI
        self.username_box = InputBox(self.x + 50, self.y + 85, 300, 40, self.font)
        self.password_box = PasswordInputBox(self.x + 50, self.y + 165, 300, 40, self.font)
        
        # Nút xác nhận & Đóng
        self.btn_submit = TextButton(self.x + 100, self.y + 250, 200, 50, "XÁC NHẬN", self.font, False)
        self.btn_close = TextButton(self.x + 360, self.y + 10, 30, 30, "X", self.font_small, False)

        # Trạng thái
        self.is_registering = False # False là Login, True là Register
        self.message = "" # Thông báo lỗi/thành công

        # Nút chuyển đổi chế độ (Tab)
        self.rect_login_tab = pygame.Rect(self.x, self.y, self.width//2, 50)
        self.rect_reg_tab = pygame.Rect(self.x + self.width//2, self.y, self.width//2, 50)

    def update(self, events):
        #Xử lý input
        for event in events:
            self.username_box.handle_event(event)
            self.password_box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                #Chọn Login / Register
                if self.rect_login_tab.collidepoint(mouse_pos):
                    self.is_registering = False
                    self.message = ""
                elif self.rect_reg_tab.collidepoint(mouse_pos):
                    self.is_registering = True
                    self.message = ""

                if self.btn_close.rect.collidepoint(mouse_pos):
                    self.manager.popup = None # Tắt popup

                if self.btn_submit.rect.collidepoint(mouse_pos):
                    username = self.username_box.text
                    password = self.password_box.text

                    if not username or not password:
                        print("Vui lòng nhập đầy đủ thông tin")
                    else:
                        if self.is_registering:
                            if self.manager.data_manager.register(username, password):
                                self.manager.popup = None

                        
                        else:
                            if self.manager.data_manager.login(username, password):
                                self.manager.popup = None

    def draw(self, screen):
        # Overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) # Màu đen trong suốt
        screen.blit(overlay, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        border_color = (100, 100, 100)
        if self.rect.collidepoint(mouse_pos):
            border_color = (0, 223, 129)
        # Vẽ nền Popup
        pygame.draw.rect(screen, (40, 40, 45), (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, border_color, (self.x, self.y, self.width, self.height), 2, border_radius=10)

        # Vẽ Tab Login/Register
        color_login = (60, 60, 65) if not self.is_registering else (30, 30, 35)
        color_reg = (60, 60, 65) if self.is_registering else (30, 30, 35)
        
        pygame.draw.rect(screen, color_login, self.rect_login_tab, border_top_left_radius=10)
        pygame.draw.rect(screen, color_reg, self.rect_reg_tab, border_top_right_radius=10)
        
        # Text cho Tab
        lbl_login = self.font.render("Đăng Nhập", True, (255,255,255) if not self.is_registering else (150,150,150))
        lbl_reg = self.font.render("Đăng Ký", True, (255,255,255) if self.is_registering else (150,150,150))
        
        screen.blit(lbl_login, (self.rect_login_tab.x + 40, self.rect_login_tab.y + 10))
        screen.blit(lbl_reg, (self.rect_reg_tab.x + 50, self.rect_reg_tab.y + 10))

        # Vẽ các Input Box và Label
        lbl_user = self.font_small.render("Tên đăng nhập:", True, (200, 200, 200))
        screen.blit(lbl_user, (self.x + 50, self.y + 55))
        self.username_box.draw(screen)

        lbl_pass = self.font_small.render("Mật khẩu:", True, (200, 200, 200))
        screen.blit(lbl_pass, (self.x + 50, self.y + 135))
        self.password_box.draw(screen)

        # 5. Nút và Thông báo
        self.btn_submit.text = "ĐĂNG KÝ" if self.is_registering else "ĐĂNG NHẬP"
        self.btn_submit.draw(screen)
        self.btn_close.draw(screen)

        if self.message:
            color = (6, 214, 160) if "thành công" in self.message else (255, 100, 100)
            msg_surf = self.font_small.render(self.message, True, color)
            # Căn giữa thông báo
            screen.blit(msg_surf, (self.x + (self.width - msg_surf.get_width())//2, self.y + 300))