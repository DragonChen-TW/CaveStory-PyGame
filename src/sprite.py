'''Sprite Module'''

import pygame
import game

class Sprite:
    def __init__(self, graphics, path, left, top, width, height):
        '''Create a sprite from the image'''
        self._image = graphics.load_image(path)
        self._source_rect = pygame.Rect(left, top, width, height)

    def draw(self, graphics, x, y):
        graphics.blit(self._image, (x, y), area=self._source_rect)

    def update(self, time_ms):
        pass
