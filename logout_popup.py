import pygame
from button import TextButton 
from assets import *

class LogoutPopup:
    def __init__(self, screen_w, screen_h, manager_ref):
        self.manager = manager_ref
        self.width, self.height = 400, 200 
        self.x = (screen_w - self.width) // 2
        self.y = (screen_h - self.height) // 2
        
        self.font = pygame.font.Font(FONT,20)
        self.font_bold = pygame.font.Font(FONT,22)

        self.btn_yes = TextButton(self.x + 35, self.y + 120, 140, 50, "CÓ", self.font, self.manager.sfx)
        self.btn_no = TextButton(self.x + 225, self.y + 120, 140, 50, "KHÔNG", self.font, self.manager.sfx)

    def draw(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # Nền Popup
        pygame.draw.rect(screen, (10, 20, 30), (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, (0, 223, 129), (self.x, self.y, self.width, self.height), 2, border_radius=10)

        # Text thông báo
        text_surf = self.font_bold.render("Bạn có chắc muốn đăng xuất?", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(self.x + self.width//2, self.y + 60))
        screen.blit(text_surf, text_rect)

        # Vẽ nút
        self.btn_yes.draw(screen)
        self.btn_no.draw(screen)

        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_just_released()[0]:
            if self.btn_no.rect.collidepoint(mouse_pos):
                self.manager.logout_popup = None
            elif self.btn_yes.rect.collidepoint(mouse_pos):
                self.manager.data_manager.current_user = None
                self.manager.logout_popup = None