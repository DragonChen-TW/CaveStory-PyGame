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

class AnimatedSprite(Sprite):
    def __init__(self, graphics, path, left, top, width, height, fps, num_frames):
        '''Create an animated sprite'''
        super().__init__(graphics, path, left, top, width, height)

        self.frame_time = 1000.0 / fps
        self.num_frames = num_frames
        self.current_frame = 0
        self.elapsed_time = 0
    
    def update(self, elapsed_time_ms):
        '''Update the sprite with based on elapsed time'''
        self.elapsed_time += elapsed_time_ms
        if self.elapsed_time > self.frame_time:
            self.current_frame += 1
            self.elapsed_time = 0

            # whether frame count inside a animation loop
            if self.current_frame < self.num_frames:
                self._source_rect.x += game.Game.tile_size
            else:
                # at the end
                self._source_rect.x -= game.Game.tile_size * (self.num_frames - 1)
                self.current_frame = 0