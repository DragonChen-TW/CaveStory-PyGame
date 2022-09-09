'''Graphic Module'''

import pygame

class Graphics:
    def __init__(self, size):
        '''Create a screen of given size'''
        self._screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        self._img_cache = {}

        # self.clear()

    def load_image(self, file_path):
        '''Load image from cache or from local'''
        if file_path not in self._img_cache:
            self._img_cache[file_path] = \
                pygame.image.load(file_path)
        return self._img_cache[file_path]

    def blit(self, source, dest, area=None, special_flag=0):
        '''Draw an image to the screen'''
        self._screen.blit(source, dest, area, special_flag)

    def flip(self):
        '''Flip the display'''
        pygame.display.flip()

    def clear(self):
        '''Clear screen with black'''
        self._screen.fill(0)
