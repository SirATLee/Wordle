import pygame
from game_data_manager import GameDataManager
from assets import *

class Game_Manager:
    def __init__(self):
        self.state = "Main Menu"
        self.game = None
        
        self.data_manager = GameDataManager()

        self.background_music = True
        self.sfx = True

        self.setting = False
        self.sub_setting = False
        self.leave_setting = False
        
        self.popup = None
        self.logout_popup = None
        self.theme = WHITE
        
        self.user_info = False
        self.overwrite_noti = False
        self.continue_popup = False

        self.leaderboard_mode = "EN"
        self.leaderboard_page = 1
