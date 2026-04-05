
import tkinter as tk
import random
import os
import winsound
import time

class SnakeFilmStar:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SNAKE PROTOCOL: THE REBIRTH")
        self.root.resizable(False, False)

        self.B_SIZE = 20
        self.W, self.H = 25, 30
        self.SAVE_FILE = "snake_checkpoint.txt"
        
        self.c = tk.Canvas(self.root, bg="black", height=self.H*self.B_SIZE, width=self.W*self.B_SIZE, highlightthickness=0)
        self.c.pack()

        # Kayıt verileri
        self.checkpoint_score = 0
        self.checkpoint_len = 3
        self.bolum = 1
        
        self.load_game_data()
        self.main_menu()
        self.root.mainloop()

    def play_sound(self, f, d):
        try: winsound.Beep(f, d)
        except: pass

    def type_text(self, text, color="#0F0", size=12, delay=40, y_pos=300, clear=True):
        if clear: self.c.delete("msg")
        full_text = ""
        for i, char in enumerate(text):
            full_text += char
            self.root.after(i * delay, lambda t=full_text: self.update_msg(t, color, size, y_pos))

    def update_msg(self, t, color, size, y_pos):
        self.c.delete("msg")
        self.c.create_text(250, y_pos, text=t, fill=color, font=("Courier", size, "bold"), tags="msg", width=420, justify="center")
        self.play_sound(600, 15)

    def save_game_data(self):
        with open(self.SAVE_FILE, "w") as f:
            f.write(f"{self.checkpoint_score},{self.checkpoint_len},{self.bolum}")

    def load_game_data(self):
        if os.path.exists(self.SAVE_FILE):
            try:
                with open(self.SAVE_FILE, "r") as f:
                    data = f.read().split(',')
                    self.checkpoint_score = int(data[0])
                    self.checkpoint_len = int(data[1])
                    self.bolum = int(data[2])
            except: pass

    def main_menu(self):
        self.c.delete("all")
        self.active = False
        self.c.create_text(250, 150, text="SNAKE\nPROTOCOL", fill="#0F0", font=("Courier", 45, "bold"), justify="center")
        
        # Yeni Oyun
        btn_new = tk.Button(self.root, text="YENİ HİKAYE", font=("Arial", 12, "bold"), bg="#0F0", width=15, command=self.intro_scene)
        self.c.create_window(250, 300, window=btn_new)

        # Devam Et
        if self.checkpoint_score > 0 or self.bolum > 1:
            btn_cont = tk.Button(self.root, text="DEVAM ET", font=("Arial", 12, "bold"), bg="#080", fg="white", width=15, command=self.start_game)
            self.c.create_window(250, 360, window=btn_cont)

    def intro_scene(self):
        self.checkpoint_score = 0
        self.checkpoint_len = 3
        self.bolum = 1
        self.c.delete("all")
        self.type_text("YIL 2026... SİSTEM ÇÖKTÜ.", "#0F0", 14, y_pos=200)
        self.root.after(3000, lambda: self.type_text("SEN, HAYATTA KALAN SON\nVERİ PARÇACIĞISIN.", "white", 12, y_pos=300))
        self.root.after(7000, lambda: self.type_text("GÖREVİN: KAYIP KODLARI TOPLA\nVE SİSTEMİ YENİDEN KUR.", "#0F0", 12, y_pos=400))
        self.root.after(11000, self.start_game)

    def start_game(self):
        self.c.delete("all")
        self.score = self.checkpoint_score
        self.snake = [[12, 15+i] for i in range(self.checkpoint_len)]
        self.dir = 'stop'
        self.active = True
        self.speed = 130
        self.apple = [random.randint(0, 24), random.randint(3, 29)]
        self.root.bind('<KeyPress>', self.handle_keys)
        self.loop()

    def handle_keys(self, e):
        k = e.keysym
        zits = {'Up':'Down', 'Down':'Up', 'Left':'Right', 'Right':'Left'}
        if k in zits and k != zits.get(self.dir): self.dir = k

    def loop(self):
        if not self.active: return

        hx, hy = self.snake[0]
        if self.dir == 'Up': hy -= 1
        elif self.dir == 'Down': hy += 1
        elif self.dir == 'Left': hx -= 1
        elif self.dir == 'Right': hx += 1

        if self.dir != 'stop':
            if hx<0 or hx>=self.W or hy<0 or hy>=self.H or [hx, hy] in self.snake:
                self.game_over_scene(); return
            
            self.snake.insert(0, [hx, hy])
            if hx == self.apple[0] and hy == self.apple[1]:
                self.score += 10
                self.play_sound(900, 40)
                self.apple = [random.randint(0, 24), random.randint(3, 29)]
            else:
                self.snake.pop()

        self.draw()
        self.root.after(self.speed, self.loop)

    def draw(self):
        self.c.delete("all")
        # Elma (Kod Parçası)
        self.c.create_oval(self.apple[0]*self.B_SIZE+4, self.apple[1]*self.B_SIZE+4, (self.apple[0]+1)*self.B_SIZE-4, (self.apple[1]+1)*self.B_SIZE-4, fill="#0FF", outline="white")
        # Yılan
        for i, (x, y) in enumerate(self.snake):
            color = "#0F0" if i == 0 else "#050"
            self.c.create_rectangle(x*self.B_SIZE, y*self.B_SIZE, (x+1)*self.B_SIZE, (y+1)*self.B_SIZE, fill=color, outline="#020")
        
        self.c.create_text(250, 20, text=f"BÖLÜM: {self.bolum} | KURTARILAN VERİ: {self.score}", fill="#0F0", font=("Courier", 10, "bold"))

    def game_over_scene(self):
        self.active = False
        self.play_sound(200, 400)
        # Mevcut durumu kaydet
        self.checkpoint_score = self.score
        self.checkpoint_len = len(self.snake)
        self.save_game_data()

        self.c.create_rectangle(40, 100, 460, 450, fill="#111", outline="red", width=2)
        self.c.create_text(250, 180, text="SİSTEM HATASI!", fill="red", font=("Courier", 24, "bold"))
        self.c.create_text(250, 230, text=f"Veri Durumu: {self.score}\nKonum Kaydedildi.", fill="white", font=("Arial", 12))

        # Seçenekler
        btn_respawn = tk.Button(self.root, text="TEKRAR DOĞ", font=("Arial", 11, "bold"), bg="#0F0", width=15, command=self.start_game)
        self.c.create_window(250, 310, window=btn_respawn)

        btn_menu = tk.Button(self.root, text="ANA MENÜ", font=("Arial", 11, "bold"), bg="#444", fg="white", width=15, command=self.main_menu)
        self.c.create_window(250, 370, window=btn_menu)

if __name__ == "__main__":
    SnakeFilmStar()