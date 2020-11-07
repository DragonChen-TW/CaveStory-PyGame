'''Game Module'''

import pygame

from graphics import Graphics
from player import Player

class Game:
    '''Game class'''

    tile_size = 32

    def __init__(self, width=640, height=480, fps=60):
        '''Initialize game with width, height and fps'''
        self.width = width
        self.height = height
        self.fps = fps
        self.size = (width, height)

        self.graphics = Graphics(self.size)
        self.clock = pygame.time.Clock()

        self.player = Player(self.graphics, 320, 240)

    def loop(self):
        '''Main game loop'''
        running = True
        while running:
            key_in = pygame.key.get_pressed()
            for event in pygame.event.get():
                # print('event', event.type)
                if event.type == pygame.QUIT:
                    running = False
            if key_in[pygame.K_ESCAPE]:
                running = False

            self.clock.tick(self.fps)

            self.update(self.clock.get_time())

            self.draw()

    def update(self, time_ms):
        '''Update object position'''
        # self.player.update(time_ms)
        pass

    def draw(self):
        '''Draw the objects'''
        self.graphics.clear()
        self.player.draw()
        self.graphics.flip()
