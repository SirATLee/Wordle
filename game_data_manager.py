import os
import pygame
import base64
from user_class import User

class GameDataManager:
    def __init__(self):
        self.file_path = "gamedata.dat"
        self.users_save_slots = []
        self.current_user = None
        self.top20_en = []  
        self.top20_vi = []  
        self.top20_eq = []
        self.load_data()
    def get_active_list(self):
        active_list = []
        for user in self.users_save_slots:
            if user.is_playing_unfinished:
                if self.current_user is not None:
                    if user.username != self.current_user.username:
                        active_list.append(user)
        return active_list


    def save_data(self):
        content = ""
        
        if self.current_user is not None:
            content += "LAST_LOGIN:" + self.current_user.username + "\n"
        else:
            content += "None\n" 
        for user in self.users_save_slots:
            user_data_str = user.get_string_data()
            content += user_data_str + "\n"


        
        
        raw_bytes = content.encode('utf-8')
        encrypted_bytes = self.xor_cipher(raw_bytes)
        final_content = base64.b64encode(encrypted_bytes)
            
        with open(self.file_path, "wb") as f:
                f.write(final_content)
    def load_data(self):
        #if not os.path.exists(self.file_path): 
         #   self.users_save_slots = []
          #  self.current_user = None
           # return
        with open(self.file_path, "rb") as f:
            file_content = f.read()

        encrypted_bytes = base64.b64decode(file_content)
        decrypted_bytes = self.xor_cipher(encrypted_bytes)

        content = decrypted_bytes.decode('utf-8')
        self.users_save_slots = []
        lines = content.strip().split("\n")
        if lines:
            if lines[0] != "None":
                last_login_name = lines[0].split(':')[1]
            else:
                last_login_name = None
            lines.pop(0)
        for line in lines:
            temp_user = User("username","password")
            temp_user.get_data_from_string(line)
            if temp_user.username == last_login_name and last_login_name is not None:
                self.current_user = temp_user
                self.current_user.last_second_time = pygame.time.get_ticks()
                print("Đã tự động đăng nhập lại")
            self.users_save_slots.append(temp_user)


    def update_top_20(self):
        pass
    def login(self, username, password):    
        for user in self.users_save_slots:
            print(user.username, user.password)
            if user.username == username and user.password == password:
                self.current_user = user
                self.current_user.last_second_time = pygame.time.get_ticks()
                return True
        print("Tên đăng nhập hoặc mật khẩu không chính xác!")
        return False
            

    def register(self,username, password): 
        for user in self.users_save_slots:
            if user.username == username:
                print("Tên đăng nhập đã tồn tại!")
                return
        if " " in username.strip(" "):
            print("Tên đăng nhập không hợp lệ")
            return
        new_user = User(username,password)
        self.users_save_slots.append(new_user)
        self.current_user = new_user
        self.save_data()
        print("Tạo tài khoản thành công!")
        return True


    def xor_cipher(self, input):
        key = b"Khoa_Bao_Mat_Sieu_Cap_Vippro_2026" 
        
        output = bytearray()
        for i in range(len(input)):
            output.append(input[i] ^ key[i % len(key)])
        return output