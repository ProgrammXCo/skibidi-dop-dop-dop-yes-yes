from PIL import Image, ImageTk
import tkinter as tk
import time
import threading
from pygame import mixer
from itertools import cycle
import signal
import os
 
class GifLabel(tk.Label):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        for i in range(im.n_frames):
            frames.append(ImageTk.PhotoImage(im.copy()))
            im.seek(i)
            
        self.frames = cycle(frames)
 
        try:
            self.delay = im.info["duration"]
        except:
            self.delay = 100
 
        if len(frames) == 1:
            self.config(image = next(self.frames))
        else:
            self.next_frame()
 
    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)

mixer.init()

class Main(tk.Tk):
    def __init__(self):
        self.path_icon = r"skibidi dop dop dop yes yes.ico"
        self.path_sound = r"skibidi dop dop dop yes yes.mp3"
        self.path_gif = r"skibidi dop dop dop yes yes.gif"
        self.path_bg = r"bg.jpg"

        super().__init__()

        self.geometry("900x500")
        self.state("zoomed")
        self.title("skibidi dop dop dop yes yes")
        self.iconbitmap(self.path_icon)

        self.protocol("WM_DELETE_WINDOW", self.exit_window)

        self.canvas = tk.Canvas(self, bg = "white", highlightthickness=0)
        self.canvas.pack(fill = "both", expand = True)
        
        self.image_bg = Image.open(self.path_bg).convert("RGBA")

        self.update()
        
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        
        self.picture_bg = ImageTk.PhotoImage(self.image_bg.resize((self.width, self.height), Image.Resampling.LANCZOS))
        self.picture_bg_tk = self.canvas.create_image(0, 0, image=self.picture_bg, anchor="nw")

        self.canvas.bind("<Configure>", self.scale_image)

        self.gif = GifLabel(self.canvas, borderwidth = 0)
        self.gif.place(x = 0, y = 0)
        self.gif.load(self.path_gif)
        self.gif.bind("<ButtonPress-1>", self.play_music)

        self.update()

        self.gif_width = self.gif.winfo_width()
        self.gif_height = self.gif.winfo_height()

        self.minsize(self.gif_width + 100, self.gif_height + 100)

        self.xspeed = 1
        self.yspeed = 1

        self.closing = False

        self.thread = threading.Thread(target = self.start)
        self.thread.start()

        self.mainloop()

    def start(self):
        self.update()
        while not self.closing:
            
            self.move()
            self.update()
            time.sleep(0.003)

        self.exit_programm()

    def exit_programm(self):
        os.kill(os.getpid(), signal.SIGINT)

    def scale_image(self, event):
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()

        self.picture_bg = ImageTk.PhotoImage(self.image_bg.resize((self.width, self.height), Image.Resampling.LANCZOS))
        self.canvas.itemconfig(self.picture_bg_tk, image = self.picture_bg)
        
    def move(self):
        self.gif.place(x = self.gif.winfo_x() + self.xspeed, y = self.gif.winfo_y() + self.yspeed)

        pos = [
            self.gif.winfo_x(), 
            self.gif.winfo_y(), 
            self.gif.winfo_x() + self.gif_width,
            self.gif.winfo_y() + self.gif_height
        ]

        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        
        if (pos[3] >= self.height and self.yspeed > 0) or (pos[1] <= 0  and self.yspeed < 0):
            self.yspeed = -1 * self.yspeed

        if (pos[2] >= self.width and self.xspeed > 0) or (pos[0] <= 0 and self.xspeed < 0):
            self.xspeed = -1 * self.xspeed

    def play_music(self, event):
        mixer.music.load(self.path_sound)
        mixer.music.play()

    def exit_window(self):
        self.closing = True

if __name__ == "__main__":
    Main()