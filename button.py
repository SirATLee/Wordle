import pygame
from assets import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Wordle")
font = pygame.font.Font(FONT,55)

button_sfx = pygame.mixer.Sound("sound/button_sfx.mp3")
button_sfx.set_volume(0.3)
class Img:
    def __init__(self, x, y, img, width, height):
        self.img = pygame.transform.scale(img, (int(width),int(height)))
        self.rect = self.img.get_rect(center = (x,y))
    def draw_button(self):
        screen.blit(self.img,self.rect)
class ImgButton:
    def __init__(self, x, y, img, width, height, sound):
        self.img = pygame.transform.scale(img, (int(width),int(height)))
        self.rect = self.img.get_rect(center = (x,y))
        self.sound = sound

    def draw_button(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.img.set_alpha(167)
            if pygame.mouse.get_just_released()[0] and self.sound:
                button_sfx.play()
        screen.blit(self.img,self.rect)

class TextButton:
    def __init__(self, x, y, width, height, text, font, sound):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.sound = sound

        self.bg_color = (15, 35, 40)
        
        self.border_color = (0, 120, 120)
        self.text_color = (200, 230, 230)
        
        self.hovered_border_color = (0, 188, 186) 
        self.hovered_text_color = (255, 255, 255)

    def draw(self, screen):
        bg_color = self.bg_color
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        if is_hovered:
            border_color = self.hovered_border_color
            text_color = self.hovered_text_color
            if pygame.mouse.get_just_released()[0] and self.sound:
                button_sfx.play()
        else:
            border_color = self.border_color
            text_color = self.text_color

        pygame.draw.rect(screen, bg_color, self.rect, border_radius=10)
        
        pygame.draw.rect(screen, border_color, self.rect, width=2, border_radius=10)
        

        text_surf = self.font.render(self.text.upper(), True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

class OptionButton:
    def __init__(self, x, y, width, height, text, mode,  value, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.mode = mode
        self.value = value 
        self.font = font
        self.indicator_rect = pygame.Rect(x + 15, y + (height - 20) // 2, 20, 20)
        self.ischosen = False

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.ischosen:
            bg_color = (40, 40, 45)
            border_color = (6, 214, 160)
            indicator_color = (6, 214, 160)
        else:
            if self.rect.collidepoint(mouse_pos):
                bg_color = (130, 130, 145) 
                border_color = (255, 209, 102) 
                indicator_color = (255, 209, 102)
            else:
                bg_color = (100, 100, 110) 
                border_color = (150, 150, 150)
                indicator_color = (255, 255, 255)
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=8)

        pygame.draw.rect(screen, border_color, self.rect, width=2, border_radius=8)

        pygame.draw.rect(screen, indicator_color, self.indicator_rect)
        pygame.draw.rect(screen, (0, 0, 0), self.indicator_rect, width=2)

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(midleft=(self.indicator_rect.right + 15, self.rect.centery))
        screen.blit(text_surf, text_rect)

def draw_nav_btn(text_str, x, y, w, h, font_name):
        mouse_pos = pygame.mouse.get_pos()
        base_rect = pygame.Rect(x, y, w, h)
        if base_rect.collidepoint(mouse_pos):
            bg_color = (200, 200, 205) 
            y_offset = 2               
            text_color = (50, 50, 50)  
        else:
            bg_color = (160, 160, 160) 
            y_offset = 5               
            text_color = (100, 100, 100) 
        draw_rect = pygame.Rect(x, y + y_offset, w, h)
        
        pygame.draw.rect(screen, bg_color, draw_rect, border_radius=10)
        pygame.draw.rect(screen, (100, 100, 100), draw_rect, 2, border_radius=10)
        text_surf = font_name.render(text_str, True, text_color)
        text_rect = text_surf.get_rect(center=draw_rect.center)
        screen.blit(text_surf, text_rect)

        
