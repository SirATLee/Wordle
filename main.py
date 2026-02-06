import pygame
import sys
import random
import base64
import game_mechanism
import game_manager
import user_class
import game_data_manager
from overwriteUI import draw_overwrite_noti
from gameUI import *
from assets import *

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("sound/background_music2.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.02)

clock = pygame.time.Clock()
manager = game_manager.Game_Manager()
while True:
    events = pygame.event.get()
    for event in events:
    
        #Xử lý lưu khi thoát game
        if event.type == pygame.QUIT:
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

        if manager.state == "Main Menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if manager.setting or manager.sub_setting or manager.leave_setting:
                        manager.setting = False
                        manager.sub_setting = False
                        manager.leave_setting = False
                    else:
                        manager.setting = True
        if manager.state == "Game Play":
            game = manager.game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if manager.setting or manager.sub_setting or manager.leave_setting:
                        manager.setting = False
                        manager.sub_setting = False
                        manager.leave_setting = False
                    else:
                        manager.sub_setting = True
                if not manager.setting and not manager.sub_setting and not manager.leave_setting:
                    if game.stop:
                        if not game.lose: 
                            game.nextword()
                    else:
                        if event.key == pygame.K_z and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                            game.undo()
                        elif event.key == pygame.K_r and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                            game.redo()
                        else:
                            if event.key == pygame.K_BACKSPACE:
                                if game.current_col > 0:
                                    game.guess_undo_stack[game.current_row].append(game.current_guesses)
                                    game.guesses[game.current_row][game.current_col - 1] = ""
                                    game.current_guesses = game.current_guesses[:-1]
                                    game.current_col -= 1
                            elif event.key == pygame.K_RETURN:
                                print(game.stages_time)
                                if game.current_col == game.word_len:
                                    if game.is_valid():
                                        game.check_guess()
                                    else:
                                        not_valid_popup(manager)
                                else:
                                    too_short_popup(manager)
                            else:
                                if game.current_col < game.word_len:
                                    if game.check_letter(event.unicode.upper()):
                                        game.guess_undo_stack[game.current_row].append(game.current_guesses)

                                        game.guesses[game.current_row][game.current_col]  = event.unicode.upper()
                                        game.current_guesses += event.unicode.upper()
                                        game.current_col += 1
                                        print(game.current_guesses)
                            #Reset Redo stack
                            game.guess_redo_stack = [[] for i in range(game.word_len + 1)]
                            game.keyboard_redo_stack = []
    
    if manager.data_manager.current_user is not None:
        manager.data_manager.current_user.time_spent_realtime_update()
    if manager.popup is not None:
            manager.popup.update(events)
                                        
    draw(manager)
    pygame.display.update()
            
