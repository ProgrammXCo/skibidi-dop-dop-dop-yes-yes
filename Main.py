from PIL import Image, ImageTk
import tkinter as tk
import sys
from pygame import mixer
from CanvasScreensaverImage import CanvasScreensaverImage

class CustomCanvasScreensaver(CanvasScreensaverImage):
    """заставка с воспроизведением звука при нажатии ЛКМ по изображению"""
    def __init__(self, canvas: tk.Canvas, image: str, sound: str, *args, **kvargs):
        self.__canvas = canvas
        self.__image = image
        self.__sound = sound

        super().__init__(canvas = self.__canvas, image = self.__image, *args, **kvargs)

        self.__canvas.tag_bind(self.id_canvas, "<ButtonPress-1>", self.__play_music)

    def __play_music(self, event):
        mixer.music.load(self.__sound)
        mixer.music.play()

class Main(tk.Tk):
    def __init__(self):
        """главный класс; главное окно"""
        super().__init__()
        
        self.withdraw()

        # инициализация микшера для воспроизведения звуков
        mixer.pre_init(44100, -16, 2, 2048)
        mixer.init()

        # ресурсы
        self.path_icon = r"icon.ico"
        self.path_sound = r"sound.mp3"
        self.path_image = r"animated_gif.gif"
        self.path_bg = r"bg.jpg"

        self.header = "skibidi dop dop yes yes"

        self.state("zoomed")
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

        # создание кастомизированной заставки
        screensaver = CustomCanvasScreensaver(canvas = self.canvas, image = self.path_image, sound = self.path_sound)
        width_screensaver, height_screensaver = screensaver.size

        self.minsize(width_screensaver + 100, height_screensaver + 100)

        self.geometry("900x500")

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
