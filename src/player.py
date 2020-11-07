'''Player Module'''

import sprite
import game

class Player:
    def __init__(self, graphics, x, y):
        self.graphics = graphics
        self.x = x
        self.y = y

        self.sprites = {}
        self.init_sprites()
        self.horizontal_facing = 0 # LEFT

    def get_sprite_state(self):
        '''Get the current sprite state'''
        return '10' # STAND, FACING_LEFT

    def init_sprites(self):
        '''Create sprites for each state'''
        tile_size = game.Game.tile_size

        # Standing, Facing LEFT
        self.sprites['00'] = \
            sprite.Sprite(
                self.graphics,
                'content/MyChar.bmp', 0, 0,
                tile_size, tile_size
            )
        
        # Moving, Facing LEFT
        self.sprites['10'] = \
            sprite.AnimatedSprite(
                self.graphics,
                'content/MyChar.bmp', 0, 0,
                tile_size, tile_size,
                15, 3
            )

    def update(self, time_ms):
        '''update the player position and animation frame'''
        self.sprites[self.get_sprite_state()].update(time_ms)

    def draw(self):
        '''Draw the player on the screen'''
        self.sprites[self.get_sprite_state()].draw(self.graphics, self.x, self.y)
