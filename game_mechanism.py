import pygame
import sys
import random
from gameplayUI import *
from assets import *
from equation_generator import *
from functions import *

class Game:
    def __init__(self, word_len, mode):
        self.mode = mode
        self.word_len = word_len
        self.type = "PRACTICE"

        self.current_row = 0
        self.current_col = 0
        self.current_guesses = ""
        self.letter_color = []

        self.remaining_undo = 3
        self.guess_undo_stack = [[] for i in range(self.word_len + 1)]
        self.guess_redo_stack = [[] for i in range(self.word_len + 1)]
        self.keyboard_undo_stack = []
        self.keyboard_redo_stack = []

        self.total_time = 180*1000
        self.total_time_remain = self.total_time
        self.game_start_time = pygame.time.get_ticks()
        self.stage_start_time = pygame.time.get_ticks()
        self.time_added = 0
        self.stages_time = []
        self.total_score = 0

        self.stop = False
        self.lose = False

        self.keyboard_switch = True

        #Xử lý các mode của game
        if self.mode == "EN" or self.mode == "VI":
            self.keyboard = [[["Q","WHITE"],["W","WHITE"],["E","WHITE"],["R","WHITE"],["T","WHITE"],["Y","WHITE"],["U","WHITE"],["I","WHITE"],["O","WHITE"],["P","WHITE"]],
                             [["A","WHITE"],["S","WHITE"],["D","WHITE"],["F","WHITE"],["G","WHITE"],["H","WHITE"],["J","WHITE"],["K","WHITE"],["L","WHITE"]],
                             [["ENTER","WHITE"],["Z","WHITE"],["X","WHITE"],["C","WHITE"],["V","WHITE"],["B","WHITE"],["N","WHITE"],["M","WHITE"],["BACKSPACE","WHITE"]]]
            if self.mode == "EN":
                self.guess_attempts = self.word_len + 1
                self.guesses = [["" for i in range(self.word_len)] for j in range(self.guess_attempts)]
                if self.word_len == 5:
                    self.secret_word = random.choice(EN5WORDS)
                elif self.word_len == 6:
                    self.secret_word = random.choice(EN6WORDS)
            else:
                self.hint = False
                self.guess_attempts = 6
                self.guesses = [["" for i in range(self.word_len)] for j in range(self.guess_attempts)]
                if self.word_len == 6:
                    self.secret_word_with_space = random.choice(VI6WORDS)
                elif self.word_len == 7:
                    self.secret_word_with_space = random.choice(VI7WORDS)
                elif self.word_len == 8:
                    self.secret_word_with_space = random.choice(VI8WORDS)

                self.secret_word = self.secret_word_with_space.replace(" ","")
        else:
            self.keyboard = [[["1","WHITE"],["2","WHITE"],["3","WHITE"],["4","WHITE"],["5","WHITE"],["6","WHITE"],["7","WHITE"],["8","WHITE"],["9","WHITE"],["0","WHITE"]],
                             [["+","WHITE"],["-","WHITE"],["*","WHITE"],["/","WHITE"],["=","WHITE"],["ENTER","WHITE"],["BACKSPACE","WHITE"]]]

            self.guess_attempts = self.word_len - 2
            self.secret_word = generate_equation(self.word_len)
            print(self.secret_word)
            self.guesses = [["" for i in range(self.word_len)] for j in range(self.guess_attempts)]
    
    #Đặt lại các biến sau khi qua từ mới
    def nextword(self):
        self.time_added += 80*1000
        self.stages_time.append(pygame.time.get_ticks() - self.stage_start_time)
        self.stage_start_time = pygame.time.get_ticks()
        self.update_score()

        self.current_row = 0
        self.current_col = 0
        self.current_guesses = ""
        self.letter_color = []

        self.guess_undo_stack = [[] for i in range(self.word_len + 1)]
        self.guess_redo_stack = [[] for i in range(self.word_len + 1)]
        self.keyboard_undo_stack = []
        self.keyboard_redo_stack = []

        self.stop = False
        self.win = False

        if self.mode == "EN" or self.mode == "VI":
            self.keyboard = [[["Q","WHITE"],["W","WHITE"],["E","WHITE"],["R","WHITE"],["T","WHITE"],["Y","WHITE"],["U","WHITE"],["I","WHITE"],["O","WHITE"],["P","WHITE"]],
                             [["A","WHITE"],["S","WHITE"],["D","WHITE"],["F","WHITE"],["G","WHITE"],["H","WHITE"],["J","WHITE"],["K","WHITE"],["L","WHITE"]],
                             [["ENTER","WHITE"],["Z","WHITE"],["X","WHITE"],["C","WHITE"],["V","WHITE"],["B","WHITE"],["N","WHITE"],["M","WHITE"],["BACKSPACE","WHITE"]]]
            if self.mode == "EN":
                self.guesses = [["" for i in range(self.word_len)] for j in range(self.guess_attempts)]
                if self.word_len == 5:
                    self.secret_word = random.choice(EN5WORDS)
                elif self.word_len == 6:
                    self.secret_word = random.choice(EN6WORDS)
            else:
                self.hint = False
                self.guesses = [["" for i in range(self.word_len)] for j in range(self.guess_attempts)]
                if self.word_len == 6:
                    self.secret_word_with_space = random.choice(VI6WORDS)
                elif self.word_len == 7:
                    self.secret_word_with_space = random.choice(VI7WORDS)
                elif self.word_len == 8:
                    self.secret_word_with_space = random.choice(VI8WORDS)

                self.secret_word = self.secret_word_with_space.replace(" ","")
        else:
            self.secret_word = generate_equation(self.word_len)
            self.guesses = [["" for i in range(self.word_len)] for j in range(self.guess_attempts)]
            self.keyboard = [[["1","WHITE"],["2","WHITE"],["3","WHITE"],["4","WHITE"],["5","WHITE"],["6","WHITE"],["7","WHITE"],["8","WHITE"],["9","WHITE"],["0","WHITE"]],
                             [["+","WHITE"],["-","WHITE"],["*","WHITE"],["/","WHITE"],["=","WHITE"],["ENTER","WHITE"],["BACKSPACE","WHITE"]]]
        print(self.secret_word)

    def load_unfinished_game(self, user):
        if not user.is_playing_unfinished:
            return
        self.mode = user.mode
        self.type = user.type
        self.secret_word = user.secret_word
        self.word_len = user.word_len
        self.stages_time = user.stages_time
        self.current_row = user.current_row
        self.current_col = user.current_col
        self.total_score = user.total_score
        # Khôi phục thời gian hiện tại
        self.game_start_time = pygame.time.get_ticks()
        self.time_added = user.remaining_time*1000 - self.total_time
        self.total_time_remain = self.total_time
        
        self.guesses = user.guesses
        self.current_guesses = user.current_guesses
        
        # Khôi phục Stack Undo/Redo 
        self.remaining_undo = user.remaining_undo
        self.guess_undo_stack = user.guess_undo_stack
        self.guess_redo_stack = user.guess_redo_stack
        
        # Reset Keyboard Stack 
        self.keyboard_undo_stack = user.keyboard_undo_stack
        self.keyboard_redo_stack = user.keyboard_redo_stack

        self.keyboard = user.keyboard
        self.letter_color = user.letter_color

        if self.mode == "VI":
            self.secret_word_with_space = user.secret_word_with_space 
            self.hint = False
            self.guess_attempts = 6
        elif self.mode == "Equation":
            self.guess_attempts = self.word_len - 2
        else:
            self.guess_attempts = self.word_len + 1
    #Kiểm tra ký tự nhập vào
    def check_letter(self, a):
        if self.mode == "EN" or self.mode == "VI":
            return a.isalpha()
        else:
            return a != "" and a in "0123456789+-*/=" 
    #Kiểm tra sự hợp lệ của từ
    def is_valid(self):
        if self.mode == "EN":
            return ((self.word_len == 5 and self.current_guesses.lower() in EN5WORDS) 
                or (self.word_len == 6 and self.current_guesses.lower() in EN6WORDS))
        elif self.mode == "VI":
            return ((self.word_len == 6 and self.current_guesses.lower() in NPVI6WORDS)
                or (self.word_len == 7 and self.current_guesses.lower() in NPVI7WORDS)
                or (self.word_len == 8 and self.current_guesses.lower() in NPVI8WORDS))
        else:
            return is_valid_equation(self.current_guesses)

    #Kiểm tra từ
    def check_guess(self):
        guess = (self.current_guesses).lower()
        if len(guess) < self.word_len:
            return
        #Tạo copy của keyboard để lưu vào stack
        snapshot_kb = [[ [key[0], key[1]] for key in row] for row in self.keyboard]
        self.keyboard_undo_stack.append(snapshot_kb)
        #Lưu kết quả đoán hiện tại vào undo stack
        self.guess_undo_stack[self.current_row].append(self.current_guesses)
        
        self.letter_color.append(["GREY"]*self.word_len)
        secret_word_list = list(self.secret_word)

        if self.mode == "VI" or self.mode == "EN":
            kb_height = 3
        else:
            kb_height = 2

        for i in range(self.word_len):
            #Kiểm tra các từ màu xanh trước
            if guess[i] == self.secret_word[i]:
                self.letter_color[self.current_row][i] = "GREEN"
                secret_word_list[i] = None

                #Cập nhật màu vào bàn phím
                for row in range(kb_height):
                    for col in range(len(self.keyboard[row])):
                        if self.keyboard[row][col][0].lower() == guess[i]:
                            self.keyboard[row][col][1] = "GREEN"
                            break

            #Kiểm tra các từ vàng
        for i in range(self.word_len):
            if guess[i] in secret_word_list and self.letter_color[self.current_row][i] == "GREY":
                self.letter_color[self.current_row][i] = "YELLOW"

                #Cập nhật màu vào bàn phím
                for row in range(kb_height):
                    for col in range(len(self.keyboard[row])):
                        if self.keyboard[row][col][0].lower() == guess[i] and self.keyboard[row][col][1] != "GREEN":
                            self.keyboard[row][col][1] = "YELLOW"
                            break
                secret_word_list.remove(guess[i])

        #Caạp nhật từ xám vào bàn phím
        for i in range(self.word_len):
            for row in range(kb_height):
                for col in range(len(self.keyboard[row])):
                    if self.keyboard[row][col][0].lower() == guess[i] and self.keyboard[row][col][1] == "WHITE":
                        self.keyboard[row][col][1] = "GREY"
        
        if guess == self.secret_word:
            self.stop = True
        elif self.current_row >= self.guess_attempts - 1:
            self.stop = True
            self.lose = True
        
        self.current_row += 1
        self.current_col = 0
        self.current_guesses = ""

    def update_score(self):
        total_score = 0
        base_score = 1000
        for i in range(len(self.stages_time)):
            stage_time = self.stages_time[i] / 1000
            
            speed_bonus = max(0,90 - stage_time)*(10 + i)
            stage_score = (base_score + speed_bonus)*(1 + i*0.2)

            total_score += stage_score
        self.total_score = total_score
    
    def undo(self):
        if len(self.guess_undo_stack[self.current_row]) != 0:
            self.guess_redo_stack[self.current_row].append(self.current_guesses)
            self.current_guesses = self.guess_undo_stack[self.current_row][-1]
            self.current_col = len(self.current_guesses)
            self.guesses[self.current_row] = list(self.current_guesses) + [""]*(self.word_len - len(self.current_guesses))
            self.guess_undo_stack[self.current_row].pop()
        else:
            if self.current_row > 0:
                if self.remaining_undo > 0:
                    self.guess_redo_stack[self.current_row].append(self.current_guesses)

                    self.current_row -= 1
                    self.current_col = self.word_len - 1    
                    self.current_guesses = self.guess_undo_stack[self.current_row][-1]

                    snapshot_kb = [[ [key[0], key[1]] for key in row] for row in self.keyboard]
                    self.keyboard_redo_stack.append(snapshot_kb)
                    self.keyboard = self.keyboard_undo_stack.pop()

                    self.remaining_undo -= 1
                else:
                    no_undo_remaining_popup()
            else:
                pass

    def redo(self):
        if len(self.guess_redo_stack[self.current_row]) != 0:
            self.guess_undo_stack[self.current_row].append(self.current_guesses)
            self.current_guesses = self.guess_redo_stack[self.current_row][-1]

            self.current_col = len(self.current_guesses)
            self.guesses[self.current_row] = list(self.current_guesses) + [""]*(self.word_len - len(self.current_guesses))
            self.guess_redo_stack[self.current_row].pop()
        else:
            if self.current_row != self.word_len:
                if len(self.guess_redo_stack[self.current_row + 1]) != 0:
                    self.remaining_undo += 1

                    snapshot_kb = [[ [key[0], key[1]] for key in row] for row in self.keyboard]
                    self.keyboard_undo_stack.append(snapshot_kb)

                    self.current_row += 1
                    self.current_guesses = self.guess_redo_stack[self.current_row][-1]
                    self.guess_redo_stack[self.current_row].pop()

                    self.current_col = len(self.current_guesses)
                    self.guesses[self.current_row] = list(self.current_guesses) + [""]*(self.word_len - len(self.current_guesses))

                    self.keyboard = self.keyboard_redo_stack[-1]
                    self.keyboard_redo_stack.pop()

                else:
                    return

        