from tkinter import *
import random
import time


class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Человечек спешит к выходу")
        self.tk.resizable(False, False)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas_width = 500
        self.canvas_height = 500
        w1 = (self.tk.winfo_screenwidth() - self.canvas_width) // 2
        h1 = (self.tk.winfo_screenheight() - self.canvas_height) // 2
        self.tk.geometry(f'{self.canvas_width}x{self.canvas_height}+{w1}+{h1}')
        self.canvas = Canvas(self.tk, width=self.canvas_width, height=self.canvas_height, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.bg = PhotoImage(file="img\\background.gif")
        w2 = self.bg.width()
        h2 = self.bg.height()
        for x in range(0, 5):
            for y in range(0, 5):
                self.canvas.create_image(x * w2, y * h2, image=self.bg, anchor='nw')
        self.sprites = []
        self.running = True

    def mainloop(self):
        while 1:
            if self.running == True:
                for sprite in self.sprites:
                    sprite.move()
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)


class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


def within_x(co1, co2):
    if (co1.x1 > co2.x1 and co1.x1 < co2.x2) \
            or (co1.x2 > co2.x1 and co1.x2 < co2.x2) \
            or (co2.x1 > co1.x1 and co2.x1 < co1.x2) \
            or (co2.x2 > co1.x1 and co2.x2 < co1.x2):
        return True
    else:
        return False


def within_y(co1, co2):
    if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
            or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
            or (co2.y1 > co1.y1 and co2.y1 < co1.y2) \
            or (co2.y2 > co1.y1 and co2.y2 < co1.y2):
        return True
    else:
        return False


def collided_left(co1, co2):
    if within_y(co1, co2):
        if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:
            return True
    return False


def collided_right(co1, co2):
    if within_y(co1, co2):
        if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
            return True
    return False


def collided_top(co1, co2):
    if within_x(co1, co2):
        if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
            return True
    return False


def collided_bottom(y, co1, co2):
    if within_x(co1, co2):
        y_calc = co1.y2 + y
        if y_calc >= co2.y1 and y_calc <= co2.y2:
            return True
    return False


class Sprite:
    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coordinates = None

    def move(self):
        pass

    def coords(self):
        return self.coordinates


class PlatformSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
        self.coordinates = Coords(x, y, x + width, y + height)


class StickFigureSprite(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.images_left = [
            PhotoImage(file="img/figure-L1.gif"),
            PhotoImage(file="img/figure-L2.gif"),
            PhotoImage(file="img/figure-L3.gif")
        ]
        self.images_right = [
            PhotoImage(file="img/figure-R1.gif"),
            PhotoImage(file="img/figure-R2.gif"),
            PhotoImage(file="img/figure-R3.gif")
        ]
        self.image = game.canvas.create_image(200, 470, image=self.images_left[0], anchor='nw')
        self.x = -2
        self.y = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)

    def turn_left(self, evt):
        if self.y == 0:
            self.x = -2

    def turn_right(self, evt):
        if self.y == 0:
            self.x = 2

    def jump(self, evt):
        if self.y == 0:
            self.y = -4
            self.jump_count = 0


if __name__ == '__main__':
    g = Game()
    platform1 = PlatformSprite(g, PhotoImage(file="img/platform1.gif"), 0, 480, 100, 10)
    platform2 = PlatformSprite(g, PhotoImage(file="img/platform1.gif"), 150, 440, 100, 10)
    platform3 = PlatformSprite(g, PhotoImage(file="img/platform1.gif"), 300, 400, 100, 10)
    platform4 = PlatformSprite(g, PhotoImage(file="img/platform1.gif"), 300, 160, 100, 10)
    platform5 = PlatformSprite(g, PhotoImage(file="img/platform2.gif"), 175, 350, 66, 10)
    platform6 = PlatformSprite(g, PhotoImage(file="img/platform2.gif"), 50, 300, 66, 10)
    platform7 = PlatformSprite(g, PhotoImage(file="img/platform2.gif"), 170, 120, 66, 10)
    platform8 = PlatformSprite(g, PhotoImage(file="img/platform2.gif"), 45, 60, 66, 10)
    platform9 = PlatformSprite(g, PhotoImage(file="img/platform3.gif"), 170, 250, 32, 10)
    platform10 = PlatformSprite(g, PhotoImage(file="img/platform3.gif"), 230, 200, 32, 10)
    g.sprites.append(platform1)
    g.sprites.append(platform2)
    g.sprites.append(platform3)
    g.sprites.append(platform4)
    g.sprites.append(platform5)
    g.sprites.append(platform6)
    g.sprites.append(platform7)
    g.sprites.append(platform8)
    g.sprites.append(platform9)
    g.sprites.append(platform10)
    g.mainloop()
