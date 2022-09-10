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

class SpriteState:
    class MotionType:
        STANDING = 0
        WALKING = 1
    
    class HorizontalFacing:
        LEFT = 0
        RIGHT = 1
    
    def __init__(self, motion_type=MotionType.STANDING, horizontal_facing=HorizontalFacing.LEFT):
        self.motion_type = motion_type
        self.horizontal_facing = horizontal_facing

    def __eq__(self, other):
        return (self.motion_type, self.horizontal_facing) == (other.motion_type, other.horizontal_facing)
    
    def __hash__(self):
        return self.motion_type * 10 + self.horizontal_facing

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

        # Sprites
        self.sprites = {}
        self.sprite_state = SpriteState(
            SpriteState.MotionType.STANDING,
            SpriteState.HorizontalFacing.LEFT,
        )
        self.init_sprites()

    def get_sprite_state(self):
        '''Get the current sprite state'''
        if self.acc_x == 0:
            self.sprite_state.motion_type = SpriteState.MotionType.STANDING
        else:
            self.sprite_state.motion_type = SpriteState.MotionType.WALKING
        return self.sprite_state

    def init_sprites(self):
        '''Create sprites for each state'''
        tile_size = game.Game.tile_size

        # STANDING, Facing LEFT
        self.sprites[SpriteState(
            SpriteState.MotionType.STANDING,
            SpriteState.HorizontalFacing.LEFT,
        )] = sprite.Sprite(
            self.graphics,
            'content/MyChar.bmp', 0, 0,
            tile_size, tile_size,
        )
        
        # WALKING, Facing LEFT
        self.sprites[SpriteState(
            SpriteState.MotionType.WALKING,
            SpriteState.HorizontalFacing.LEFT,
        )] = sprite.AnimatedSprite(
            self.graphics,
            'content/MyChar.bmp', 0, 0,
            tile_size, tile_size,
            15, 3
        )

        # STANDING, Facing RIGHT
        self.sprites[SpriteState(
            SpriteState.MotionType.STANDING,
            SpriteState.HorizontalFacing.RIGHT,
        )] = sprite.Sprite(
            self.graphics,
            'content/MyChar.bmp', 0, tile_size,
            tile_size, tile_size,
        )
        
        # WALKING, Facing RIGHT
        self.sprites[SpriteState(
            SpriteState.MotionType.WALKING,
            SpriteState.HorizontalFacing.RIGHT,
        )] = sprite.AnimatedSprite(
            self.graphics,
            'content/MyChar.bmp', 0, tile_size,
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
        self.sprite_state.horizontal_facing = SpriteState.HorizontalFacing.LEFT
        self.acc_x = -WALK_ACCELERATION

    def start_moving_right(self):
        self.sprite_state.horizontal_facing = SpriteState.HorizontalFacing.RIGHT
        self.acc_x = WALK_ACCELERATION

    def stop_moving(self):
        self.acc_x = 0.0