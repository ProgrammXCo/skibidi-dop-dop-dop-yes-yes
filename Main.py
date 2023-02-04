from PIL import Image, ImageTk
import tkinter as tk
import sys
from CanvasScreensaverImage import CanvasScreensaver

class Main(tk.Tk):
    """главный класс"""
    def __init__(self):
        super().__init__()
        
        self.withdraw() # спрятать окно

        # ресурсы
        self.path_icon = r"icon.ico"
        self.path_sound = r"sound.mp3"
        self.path_image = r"animated_gif.gif"
        self.path_bg = r"bg.jpg"

        self.header = "skibidi dop dop yes yes"

        self.state("zoomed") # развернуть окно
        self.title(self.header)
        self.iconbitmap(self.path_icon)

        self.protocol("WM_DELETE_WINDOW", self.exit_window) # ослеживать нажание на кнопку закрыть окно

        self.canvas = tk.Canvas(self, bg = "white", highlightthickness = 0)
        self.canvas.pack(fill = "both", expand = True)
  
        self.update()
        
        width_canvas = self.canvas.winfo_width()
        height_canvas = self.canvas.winfo_height()
        
        # создание фонового изображения на холст и масштабирование под размер холста
        self.image_bg = Image.open(self.path_bg).convert("RGBA")
        self.picture_bg = ImageTk.PhotoImage(self.image_bg.resize((width_canvas, height_canvas), Image.Resampling.LANCZOS))
        self.picture_bg_tk = self.canvas.create_image(0, 0, image = self.picture_bg, anchor = "nw")

        self.canvas.bind("<Configure>", self.scale_image)

        # создание заставки
        screensaver = CanvasScreensaver(canvas = self.canvas, image = self.path_image, sound = self.path_sound)
        width_screensaver, height_screensaver = screensaver.size

        self.minsize(width_screensaver + 100, height_screensaver + 100)

        self.geometry("900x500") # показать окно

        self.mainloop()

    def scale_image(self, event):
        """масштабирование фона под размер холста"""
        width_canvas = self.canvas.winfo_width()
        height_canvas = self.canvas.winfo_height()

        self.picture_bg = ImageTk.PhotoImage(self.image_bg.resize((width_canvas, height_canvas), Image.Resampling.LANCZOS))
        self.canvas.itemconfig(self.picture_bg_tk, image = self.picture_bg)

    def exit_window(self):
        """выход из программы"""
        sys.exit()

if __name__ == "__main__":
    Main()
