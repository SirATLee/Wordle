import pygame
import time
import base64
from gameplayUI import get_remaining_time
from assets import *

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.total_exp = 0
        self.time_spent = 0
        #Mode Stats [Best Score, Avg Score, Best Streak, Số lượt đã chơi, Số lượng từ đã đoán được]
        self.stats_en = [0,0,0,0,0]
        self.stats_vi = [0,0,0,0,0]
        self.stats_eq = [0,0,0,0,0]
    
        #
        self.is_practice_mode = False
        self.ranked_lives = 3
        self.last_life_regen = time.time()        
        ##                     ##

        #Biến để cập nhật thời gian
        self.last_second_time = pygame.time.get_ticks()

        #Thông tin chơi dở (nếu có)
        self.saved_game_string = ""
        self.is_playing_unfinished = False
        self.is_updated = False

    def update_after_game(self, mode, score, streak, type):
        self.total_exp += score
        if type == "RANK":
            if mode == "EN":
                if score > self.stats_en[0]: self.stats_en[0] = score
                if streak > self.stats_en[2]: self.stats_en[2] = streak

                total_score = self.stats_en[1]*self.stats_en[3] + score
                self.stats_en[3] += 1
                self.stats_en[1] = total_score//self.stats_en[3]
                self.stats_en[4] += streak
            elif mode == "VI":
                if score > self.stats_vi[0]: self.stats_vi[0] = score
                if streak > self.stats_vi[2]: self.stats_vi[2] = streak

                total_score = self.stats_vi[1]*self.stats_vi[3] + score
                self.stats_vi[3] += 1
                self.stats_vi[1] = round(total_score/self.stats_vi[3],1)
                self.stats_vi[4] += streak
            elif mode == "Equation":
                if score > self.stats_eq[0]: self.stats_eq[0] = score
                if streak > self.stats_eq[2]: self.stats_eq[2] = streak

                total_score = self.stats_eq[1]*self.stats_eq[3] + score
                self.stats_eq[3] += 1
                self.stats_eq[1] = round(total_score/self.stats_eq[3],1)
                self.stats_eq[4] += streak
    def update_lives(self):
        if self.ranked_lives < 3:
            current_time = time.time()
            regen_interval = 28800 
            time_passed = current_time - self.last_life_regen
            
            if time_passed >= regen_interval:
                # Tính số mạng được hồi
                lives_to_add = int(time_passed // regen_interval)
                
                self.ranked_lives = min(3, self.ranked_lives + lives_to_add)
                
                # Cập nhật lại mốc thời gian 
                self.last_life_regen += lives_to_add * regen_interval
                
        # Nếu đã đầy mạng thì reset mốc thời gian về hiện tại để chờ lần mất tiếp theo
        if self.ranked_lives >= 3:
            self.last_life_regen = time.time()
    def keyboard_to_str(self,keyboard):
        kb_data_list = []
        for row in keyboard:
            for key_item in row:
                kb_data_list.append(f"{key_item[0]}:{key_item[1]}")
            
        return ",".join(kb_data_list)
    
    def str_to_keyboard(self, kb_str, mode):
        keyboard_items = kb_str.split(",")
        if mode == "Equation":
            keyboard = [[],[]]
            row = 0
            for item in keyboard_items:
                if ":" in item:
                    keyboard[row].append(item.split(":"))
                    if item.split(":")[0] == "0":
                        row += 1
        else:
            keyboard = [[],[],[]]
            row = 0
            for item in keyboard_items:
                if ":" in item:
                    keyboard[row].append(item.split(":"))
                    if item.split(":")[0] == "P" or item.split(":")[0] == "L" :
                        row += 1

        return keyboard
    
    def stack_to_str(self, stack):
        rows_str = []
        for row_list in stack:
            row_data = ",".join(row_list) 
            if not row_data: row_data = "EMPTY" 
            rows_str.append(row_data)
        return ">>>".join(rows_str)
    
    def str_to_stack(self, stack_str):
        stack = []
        if not stack_str: return stack
        rows = stack_str.split(">>>")
        for r in rows:
            if r == "EMPTY":
                stack.append([])
            else:
                stack.append(r.split(","))
        return stack
    def kb_stack_to_str(self, stack):
        if stack == [] : return ""
        items = []
        for kb in stack:
            items.append(self.keyboard_to_str(kb)) 
        return "###".join(items)

    def str_to_kb_stack_data(self, stack_str, mode):
        data_stack = []
        if not stack_str: return data_stack
        items = stack_str.split("###")
        for item in items:
                data_stack.append(self.str_to_keyboard(item, mode)) 
        return data_stack
    
    def save_unfinished_game(self,manager):
        game = manager.game
        self.is_playing_unfinished = True

        remaining_time = get_remaining_time(manager)

        if game.stages_time:
            stages_time_str = "-".join(map(str, game.stages_time))
        else:
            stages_time_str = "" 
        guesses_str = self.stack_to_str(game.guesses)

        current_kb_str = self.keyboard_to_str(game.keyboard)
        current_kb_undo_stack_str = self.kb_stack_to_str(game.keyboard_undo_stack)
        current_kb_redo_stack_str = self.kb_stack_to_str(game.keyboard_redo_stack)

        guess_undo_str = self.stack_to_str(game.guess_undo_stack)
        guess_redo_str = self.stack_to_str(game.guess_redo_stack)

        letter_color_str = self.stack_to_str(game.letter_color)
        #Thứ tự: Mode | Word | Row | Col | Time | Guesses | CurrentGuess | Keyboard | GuessUndo | GuessRedo | RemainingUndo | Letter Color
        self.saved_game_string = (
            f"{game.mode}|||"
            f"{game.secret_word}|||"
            f"{game.word_len}|||"
            f"{stages_time_str}|||"
            f"{game.current_row}|||"
            f"{game.current_col}|||"
            f"{remaining_time}|||"
            f"{guesses_str}|||"
            f"{game.current_guesses}|||"
            f"{current_kb_str}|||"
            f"{current_kb_undo_stack_str}|||" 
            f"{current_kb_redo_stack_str}|||"        
            f"{guess_undo_str}|||"       
            f"{guess_redo_str}|||"       
            f"{game.remaining_undo}|||"  
            f"{letter_color_str}|||"
            f"{game.total_score}|||"
            f"{game.time_added}|||"
            f"{game.type}"  
        )
        if game.mode == "VI":
            self.saved_game_string += f"|||{game.secret_word_with_space}"
    def get_string_data(self):
        stats_en_str = "-".join(map(str, self.stats_en))
        stats_vi_str = "-".join(map(str, self.stats_vi))
        stats_eq_str = "-".join(map(str, self.stats_eq))
        
        data = [
            self.username,
            self.password,
            str(self.total_exp),
            str(self.time_spent),
            stats_en_str,
            stats_vi_str,
            stats_eq_str,
            str(self.ranked_lives),
            str(self.last_life_regen),
            str(self.is_practice_mode),

            str(self.is_playing_unfinished)
        ]

        base_data = ";".join(data)

        if self.is_playing_unfinished:
            
            return f"{base_data};{self.saved_game_string}"
        
        return base_data
    

    def get_data_from_string(self, data_str):
        if not data_str: return

        data_parts = data_str.split(";")
        self.username = data_parts[0]
        self.password = data_parts[1]
        self.total_exp = int(data_parts[2])
        self.time_spent = int(data_parts[3])

        self.stats_en = [float(i) for i in data_parts[4].split("-")]
        self.stats_vi = [float(i) for i in data_parts[5].split("-")]
        self.stats_eq = [float(i) for i in data_parts[6].split("-")]

        self.ranked_lives = int(data_parts[7])
        self.last_life_regen = float(data_parts[8])
        self.is_practice_mode = (data_parts[9] == "True")
        if data_parts[10].strip() == "True": 
            self.is_playing_unfinished = True
        else: 
            self.is_playing_unfinished = False


        if self.is_playing_unfinished and len(data_parts) > 11:
            self.saved_game_string = data_parts[11]
            game_parts = data_parts[11].split("|||")
            
            self.mode = game_parts[0]
            self.secret_word = game_parts[1]
            self.word_len = int(game_parts[2])
            if game_parts[3]:
                self.stages_time = [int(i) for i in game_parts[3].split("-")]
            else:
                self.stages_time = []
            self.current_row = int(game_parts[4])
            self.current_col = int(game_parts[5])
            self.remaining_time = int(game_parts[6])
            self.guesses = self.str_to_stack(game_parts[7])
            self.current_guesses = game_parts[8]
            
                # Load Bàn phím 
            self.keyboard = self.str_to_keyboard(game_parts[9],self.mode)
            self.keyboard_undo_stack = self.str_to_kb_stack_data(game_parts[10],self.mode)
            self.keyboard_redo_stack = self.str_to_kb_stack_data(game_parts[11],self.mode)
                # Load Stack 
            self.guess_undo_stack = self.str_to_stack(game_parts[12])
            self.guess_redo_stack = self.str_to_stack(game_parts[13])
                
            self.remaining_undo = int(game_parts[14])
            self.letter_color = self.str_to_stack(game_parts[15])
            self.total_score = float(game_parts[16])
            self.time_added = float(game_parts[17])
            self.type = game_parts[18]
            if self.mode == "VI":
                self.secret_word_with_space = game_parts[19]

    def time_spent_realtime_update(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_second_time >= 1000:
                self.time_spent += 1  
                self.last_second_time = current_time             






        
        


