from PIL import Image, ImageTk
import tkinter as tk
import time
import sys
from pygame import mixer
from itertools import cycle
 
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

class Main():
    def __init__(self, root: tk.Tk):
        self.path_icon = r"skibidi dop dop dop yes yes.ico"

        self.root = root
        self.root.geometry("600x600")
        self.root.state("zoomed")
        self.root.title("skibidi dop dop dop yes yes")
        self.root.iconbitmap(self.path_icon)

        self.root.protocol("WM_DELETE_WINDOW", self.exit_window)

        self.canvas = tk.Canvas(root, bg = "white", highlightthickness=0)
        self.canvas.pack(fill = "both", expand = True)

        self.path_sound = r"skibidi dop dop dop yes yes.mp3"
        self.path_gif = r"skibidi dop dop dop yes yes.gif"
        self.path_bg = r"bg.jfif"
        
        self.image_bg = Image.open(self.path_bg).convert("RGBA")

        self.root.update()
        
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        
        self.picture_bg = ImageTk.PhotoImage(self.image_bg.resize((self.width, self.height), Image.Resampling.LANCZOS))
        self.picture_bg_tk = self.canvas.create_image(0, 0, image=self.picture_bg, anchor="nw")

        self.gif = GifLabel(self.canvas, borderwidth = 0)
        self.gif.place(x = 0, y = 0)
        self.gif.load(self.path_gif)
        self.gif.bind("<ButtonPress-1>", self.play_music)

        self.root.update()

        self.gif_width = self.gif.winfo_width()
        self.gif_height = self.gif.winfo_height()

        self.xspeed = 1
        self.yspeed = 1

        self.closing = False

        self.root.update()
        
        while not self.closing:
            self.move()
            self.root.update()
            time.sleep(0.003)

        sys.exit()
        
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
    root = tk.Tk()

    Main(root)

    root.mainloop()
