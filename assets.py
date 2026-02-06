
#Font
FONT = "Font.ttf"

#Wordlist
    #EN
with open("Words/EN5.txt") as f:
    EN5WORDS = [line.strip() for line in f]
with open("Words/EN6.txt") as f:
    EN6WORDS = [line.strip() for line in f]
    #VI
with open("Words/VI6.txt",encoding='utf-8') as f:
    VI6WORDS = [line.strip() for line in f]
with open("Words/VI7.txt",encoding='utf-8') as f:
    VI7WORDS = [line.strip() for line in f]
with open("Words/VI8.txt",encoding='utf-8') as f:
    VI8WORDS = [line.strip() for line in f]
with open("Words/VI6_NOSPACE.txt",encoding='utf-8') as f:
    NPVI6WORDS = [line.strip() for line in f]
with open("Words/VI7_NOSPACE.txt",encoding='utf-8') as f:
    NPVI7WORDS = [line.strip() for line in f]
with open("Words/VI8_NOSPACE.txt",encoding='utf-8') as f:
    NPVI8WORDS = [line.strip() for line in f]

# Color
GREY = (70, 70, 80)
WHITE_GREY = (222, 222, 222)
GREEN = (6, 214, 160)
YELLOW = (255, 209, 102)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
OUTLINE = (100, 100, 100)
FILLED_OUTLINE = (150, 150, 150)
DARK_BG = (30, 30, 30)
NEON_GREEN = (0, 230, 150)
WHITE = (255, 255, 255)
GRAY_TEXT = (150, 150, 150)
TAB_INACTIVE = (50, 50, 50)
TAB_ACTIVE = NEON_GREEN
COC_BG_PANEL = (210, 210, 215)  
COC_ROW_BG = (245, 245, 245)    
COC_YELLOW = (255, 215, 0)       
COC_SILVER = (192, 192, 192)     
COC_BRONZE = (205, 127, 50)      
COC_DARK_TEXT = (50, 50, 50)
COC_GREEN_TEXT = (0, 150, 0)     
SHADOW = (150, 150, 150)
# Kích thước
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 1000
TILE_SIZE = 70
KEYBOARD_TILE_WIDTH = 65
KEYBOARD_TILE_HEIGHT = 80
MARGIN = 10
T_MARGIN = 100
BOTTOM_MARGIN = 100 
LR_MARGIN = 100
