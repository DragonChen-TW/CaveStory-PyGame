'''Player Module'''

import sprite
import game

# Movement Constants
# MAX_DASH = 812 / 4
# MAX_MOVE = 1535 / 4
# DASH_GROUND = 85 / 4
# RESIST = 51 / 4

WALK_ACCELERATION = 0.0012  # pixels / ms / ms
MAX_MOVE = 0.325            # pixels / ms
SLOWDOWN_FACTOR = 0.75      # ratio
# End of Movement Constants

class Player:
    def __init__(self, graphics, x, y, vel_x, vel_y):
        self.graphics = graphics
        self.x = x
        self.y = y
        self.acc_x = 0.0
        self.vel_x = vel_x
        self.vel_y = vel_y
        
        # Movement Flags
        self.moving_left = False
        self.moving_right = False

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

        self.x += round(self.vel_x * time_ms)
        self.vel_x += self.acc_x * time_ms

        # Add Physics Resist
        if self.acc_x < 0:      # to left
            self.vel_x = max(self.vel_x, -MAX_MOVE)
        elif self.acc_x > 0:    # to right
            self.vel_x = min(self.vel_x, MAX_MOVE)
        else:
            self.vel_x *= SLOWDOWN_FACTOR
    
        # Boundary
        if self.x < 0:
            self.x = 0
        if self.x > 640 - 32:
            self.x = 640 - 32

    def draw(self):
        '''Draw the player on the screen'''
        self.sprites[self.get_sprite_state()].draw(self.graphics, self.x, self.y)

    # Moving Functions
    def start_moving_left(self):
        self.acc_x = -WALK_ACCELERATION

    def start_moving_right(self):
        self.acc_x = WALK_ACCELERATION

    def stop_moving(self):
        self.acc_x = 0.0