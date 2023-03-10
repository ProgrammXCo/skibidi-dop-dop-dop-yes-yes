from PIL import Image, ImageTk
import tkinter as tk
from itertools import count
from pygame import mixer

class CanvasImage():
    """заставка на холст tk, позволяющая отображать изображения и анимированные gif"""
    def __init__(self, canvas: tk.Canvas, image: str, x: int = 0, y: int = 0):
        self.__canvas = canvas
        self.__x = x
        self.__y = y
        if isinstance(image, str):
            image = Image.open(image)
        self.__loc = 0
        self.__frames = []

        try:
            for i in count(1):
                self.__frames.append(ImageTk.PhotoImage(image.copy()))
                image.seek(i)
        except EOFError:
            pass

        self.__len_frame = len(self.__frames)

        try:
            self.__delay_anim = image.info["duration"]
        except:
            self.__delay_anim = 100

        if len(self.__frames) > 0:
            self.__screensaver = self.__canvas.create_image(self.__x, self.__y, image = self.__frames[0], anchor = tk.NW)
            self.__size_screensaver = [self.__frames[0].width(), self.__frames[0].height()]

            if len(self.__frames) > 1:
                self.__canvas.after(self.__delay_anim, self.__next_frame)

    @property 
    def id_canvas(self) -> int:
        """возвращает id объекта на холсте"""
        return self.__screensaver

    @property 
    def size(self) -> list:
        """возвращает размер изображения в пикселях"""
        return self.__size_screensaver
    
    @property 
    def x(self) -> int:
        """возвращает x"""
        return self.__x

    @property 
    def y(self) -> int:
        """возвращает y"""
        return self.__y

    def __next_frame(self):
        """новый кадр в анимировананных gif"""
        self.__loc = (self.__loc + 1) % self.__len_frame
        self.__canvas.itemconfig(self.__screensaver, image = self.__frames[self.__loc])
        self.__canvas.after(self.__delay_anim, self.__next_frame)

class CanvasScreensaver(CanvasImage):
    """заставка с движением и воспроизведением звука при нажатии ЛКМ по изображению"""

    # инициализация микшера для воспроизведения звуков
    mixer.pre_init(44100, -16, 8, 2048)
    mixer.init()
    channel = -1

    def __init__(self, canvas: tk.Canvas, image: str, sound: str, x: int = 0, y: int = 0, x_speed: int = 0.8, y_speed: int = 0.8):
        self.__canvas = canvas
        self.__sound = sound
        self.__image = image
        self.__x = x
        self.__y = y
        self.__x_speed = x_speed
        self.__y_speed = y_speed
        self.__delay_move = 3

        CanvasScreensaver.channel += 1
        self.__channel = mixer.Channel(CanvasScreensaver.channel)

        super().__init__(canvas = self.__canvas, image = self.__image)

        self.__canvas.tag_bind(self.id_canvas, "<ButtonPress-1>", self.__play_music) # ЛКМ
        self.__canvas.tag_bind(self.id_canvas, "<ButtonPress-2>", self.__play_music) # СКМ
        self.__canvas.tag_bind(self.id_canvas, "<ButtonPress-3>", self.__play_music) # ПКМ

        self.__canvas.after(self.__delay_move, lambda: (self.move(self.__x + self.__x_speed, self.__y + self.__y_speed)))

    @property 
    def x_speed(self) -> int:
        """возвращает скорость по горизонтали"""
        return self.__x_speed

    @property 
    def y_speed(self) -> int:
        """возвращает скорость по вертикали"""
        return self.__x_speed

    @x_speed.setter 
    def x_speed(self, x_speed: int):
        """устанавливает новую скорость по горизонтали"""
        self.__x_speed = x_speed

    @y_speed.setter 
    def y_speed(self, y_speed: int):
        """устанавливает новую скорость по вертикали"""
        self.__y_speed = y_speed

    def move(self, x: int, y: int):
        """изменить координату изображения на холсте"""
        self.__x = x
        self.__y = y

        self.__canvas.coords(self.id_canvas, self.__x, self.__y)

        pos = self.__canvas.bbox(self.id_canvas)

        width_canvas = self.__canvas.winfo_width()
        height_canvas = self.__canvas.winfo_height()

        if (pos[2] >= width_canvas and self.__x_speed > 0) or (pos[0] <= 0 and self.__x_speed < 0):
            self.__x_speed = -1 * self.__x_speed

        if (pos[3] >= height_canvas and self.__y_speed > 0) or (pos[1] <= 0  and self.__y_speed < 0):
            self.__y_speed = -1 * self.__y_speed

        self.__canvas.after(self.__delay_move, lambda:(self.move(self.__x + self.__x_speed, self.__y + self.__y_speed)))

    def __play_music(self, event):
        sound = mixer.Sound(self.__sound)
        self.__channel.play(sound)
