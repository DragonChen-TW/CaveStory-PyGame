'''Game Module'''

import pygame

from graphics import Graphics
from player import Player

class Game:
    tile_size = 32

    def __init__(self, width=640, height=480, fps=60):
        '''Initialize game with width, height and fps'''
        self.width = width
        self.height = height
        self.fps = fps
        self.size = (width, height)

        pygame.init()
        pygame.display.set_mode(self.size)
        print('init')

        self.graphics = Graphics(self.size)
        self.clock = pygame.time.Clock()

        self.player = Player(self.graphics, 320, 240,
            0, 0
        )

    def loop(self):
        '''Main game loop'''
        running = True
        while running:
            key_in = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    running = False
                
                # Player Jump
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        self.player.start_jump()
                    elif event.type == pygame.KEYUP and event.key == pygame.K_x:
                        self.player.stop_jump()

            if key_in[pygame.K_ESCAPE]:
                running = False
            
            # Horizonal movement
            if key_in[pygame.K_LEFT] and key_in[pygame.K_RIGHT]:
                self.player.stop_moving()
            elif key_in[pygame.K_LEFT]:
                self.player.start_moving_left()
            elif key_in[pygame.K_RIGHT]:
                self.player.start_moving_right()
            else:
                self.player.stop_moving()

            self.clock.tick(self.fps)

            self.update(self.clock.get_time())

            self.draw()

    def update(self, time_ms):
        '''Update object position'''
        self.player.update(time_ms)

    def draw(self):
        '''Draw the objects'''
        self.graphics.clear()
        self.player.draw()
        self.graphics.flip()
