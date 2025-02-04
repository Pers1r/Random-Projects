import pygame
import os
import pygame as pg
from random import choice, randrange


class Symbol:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.value = choice(green_katakana)
        self.interval = randrange(4, 30)

    def draw(self, color):
        frames = pg.time.get_ticks()
        if not frames % self.interval:
            self.value = choice(green_katakana if color == "green" else lightgreen_katakana)
        self.y = self.y + self.speed if self.y < HEIGHT else -FONT_SIZE
        window.blit(self.value, (self.x, self.y))


class SymbolCol:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.quantity = randrange(8, 20)
        self.speed = randrange(3, 10)
        self.symbols = [Symbol(self.x, i, self.speed) for i in range(self.y, self.y-FONT_SIZE*self.quantity, -FONT_SIZE)]

    def draw(self):
        [symbol.draw("green") if i else symbol.draw("lightgreen") for i, symbol in enumerate(self.symbols)]




katakana = [chr(int("0x30a0", 16) + i) for i in range(96)]
pygame.init()
RES = WIDTH, HEIGHT = 1600, 900
FONT_SIZE = 40
alpha_value = 0
surface = pg.display.set_mode(RES)
window = pg.Surface(RES)
window.set_alpha(alpha_value)
clock = pg.time.Clock()
font = pg.font.Font("ipaexg.ttf", FONT_SIZE)
green_katakana = [font.render(char, True, (0, randrange(160, 255), 0)) for char in katakana]
lightgreen_katakana = [font.render(char, True, pg.Color("lightgreen")) for char in katakana]
symbol_columns = [SymbolCol(x, randrange(-HEIGHT, 0)) for x in range(0, WIDTH, FONT_SIZE)]

print(green_katakana[0])
while True:
    surface.blit(window, (0, 0))
    window.fill(pg.Color("black"))

    if not pg.time.get_ticks() % 20 and alpha_value < 150:
        alpha_value += 3
        window.set_alpha(alpha_value)

    # pg.display.set_caption(f"FPS: {round(clock.get_fps(), 1)}")
    [exit() for e in pg.event.get() if e.type == pg.QUIT]
    [symbol_column.draw()for symbol_column in symbol_columns]
    pg.display.flip()
    clock.tick(60)
