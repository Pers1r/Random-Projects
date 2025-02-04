import copy
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
import sys
import random

pygame.init()

WIDTH = 1000
HEIGHT = 700
WINDOW_HEIGHT = 700
BLOCK_SIZE = 20
FPS = 60
BORN = [3]
SURVIVE = [2, 3]


class Window:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game of Life")
        self.clock = pygame.time.Clock()
        self.slider = Slider(self.window, 400, 670, 200, 10, min=1, max=50, step=1)
        self.start_button = Button(self.window, 0, 650, 70, 50,
                                   text="Start", onClick=self.start_life, fontSize=15, radius=20)
        self.reset_button = Button(self.window, 80, 650, 70, 50,
                                   text="Reset", onClick=self.reset, fontSize=15, radius=20)
        self.random_button = Button(self.window, 160, 650, 70, 50,
                                    text="Random", onClick=self.random_pos, fontSize=15, radius=20)
        self.tiles = [[0 for _ in range(WIDTH//BLOCK_SIZE)] for _ in range(WINDOW_HEIGHT//BLOCK_SIZE)]
        self.mouse = pygame.mouse.get_pos()
        self.running = False

    def mainloop(self):
        last_update_time = pygame.time.get_ticks()
        while True:
            self.clock.tick(FPS)
            self.mouse = pygame.mouse.get_pos()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            simulation_speed = 1000 - self.slider.getValue() * 20

            curr_time = pygame.time.get_ticks()
            if self.running and curr_time - last_update_time >= simulation_speed:
                self.life()
                last_update_time = curr_time

            self.draw_grid(events)

    def random_pos(self):
        if not self.running:
            for row in range(WINDOW_HEIGHT//BLOCK_SIZE):
                for col in range(WIDTH//BLOCK_SIZE):
                    self.tiles[row][col] = random.randint(0, 1)

    def reset(self):
        self.running = False
        self.tiles = [[0 for _ in range(WIDTH//BLOCK_SIZE)] for _ in range(WINDOW_HEIGHT//BLOCK_SIZE)]

    def start_life(self):
        self.running = True

    def draw_grid(self, events):
        self.window.fill((255, 255, 255))
        height = 0
        width = 0
        while height < WINDOW_HEIGHT:
            height += BLOCK_SIZE
            pygame.draw.line(self.window, (10, 10, 10), (0, height), (WIDTH, height))
        while width < WIDTH:
            width += BLOCK_SIZE
            pygame.draw.line(self.window, (10, 10, 10), (width, 0), (width, WINDOW_HEIGHT))
        pygame.draw.line(self.window, (0, 0, 0), (0, WINDOW_HEIGHT), (WIDTH, WINDOW_HEIGHT), width=3)

        x = int(self.mouse[0]/BLOCK_SIZE)
        y = int(self.mouse[1]/BLOCK_SIZE)
        if not self.running:
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.create_tile(x, y)

            if pygame.mouse.get_pressed(num_buttons=3)[2]:
                self.delete_tile(x, y)
        self.draw_tiles()
        pygame_widgets.update(events)
        pygame.display.update()

    def draw_tiles(self):
        for row in range(WINDOW_HEIGHT//BLOCK_SIZE):
            for col in range(WIDTH//BLOCK_SIZE):
                if self.tiles[row][col] == 1:
                    pygame.draw.rect(self.window, (0, 0, 0),
                                     (col*BLOCK_SIZE, row*BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

    def create_tile(self, x, y):
        if 0 <= x < WIDTH / BLOCK_SIZE and 0 <= y < WINDOW_HEIGHT / BLOCK_SIZE:
            self.tiles[y][x] = 1
            pygame.draw.rect(self.window, (0, 0, 0),
                             (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE,
                              BLOCK_SIZE))

    def delete_tile(self, x, y):
        if 0 <= x < WIDTH / BLOCK_SIZE and 0 <= y < WINDOW_HEIGHT / BLOCK_SIZE:
            self.tiles[y][x] = 0

    def get_sum(self, x, y):
        close = 0
        br = self.tiles
        width, height = len(br[0]), len(br)

        directions = [
            (-1, -1), (-1, 0), (-1, 1),  # Top-left, top, top-right
            (0, -1),         (0, 1),    # Left,      right
            (1, -1), (1, 0), (1, 1)     # Bottom-left, bottom, bottom-right
        ]

        for dx, dy in directions:
            nx, ny = (x + dx) % width, (y + dy) % height
            close += br[ny][nx]

        return close

    def life(self):
        br = self.tiles
        width, height = len(br[0]), len(br)
        new_grid = copy.deepcopy(self.tiles)
        for row in range(height):
            for col in range(width):
                if br[row][col] == 0 and self.get_sum(col, row) in BORN:
                    new_grid[row][col] = 1
                if br[row][col] == 1 and self.get_sum(col, row) not in SURVIVE:
                    new_grid[row][col] = 0
        self.tiles = new_grid



Window().mainloop()
