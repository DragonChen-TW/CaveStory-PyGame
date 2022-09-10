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
SLOWDOWN_FACTOR = 0.85      # ratio

JUMP_TIME = 275
GRAVITY = 0.0012
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

class Jump:
    def __init__(self):
        self.time_remaining = 0
        self.active = False
    
    def update(self, elapsed_time):
        if self.active:
            self.time_remaining -= elapsed_time
            if self.time_remaining <= 0:
                self.active = False

    def reset(self):
        self.time_remaining = JUMP_TIME
        self.reactivate()
    
    def reactivate(self):
        self.active = self.time_remaining > 0
    
    def deactivate(self):
        self.active = False

class Player:
    def __init__(self, graphics, x, y, vel_x, vel_y):
        self.graphics = graphics
        self.x = x
        self.y = y
        self.acc_x = 0.0
        self.acc_y = 0.0
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

        # Jump
        self.jump = Jump()

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
        self.jump.update(time_ms)
        self.sprites[self.get_sprite_state()].update(time_ms)

        self.x += round(self.vel_x * time_ms)
        self.vel_x += self.acc_x * time_ms

        # Add Physics Resist
        if self.acc_x < 0:      # to left
            self.vel_x = max(self.vel_x, -MAX_MOVE)
        elif self.acc_x > 0:    # to right
            self.vel_x = min(self.vel_x, MAX_MOVE)
        elif self.on_ground():
            self.vel_x *= SLOWDOWN_FACTOR
        
        # Jump
        self.y += round(self.vel_y * time_ms)
        if not self.jump.active:
            self.vel_y = min(
                self.vel_y + GRAVITY * time_ms,
                MAX_MOVE
            )

        # TODO: remove this hack
        if self.y >= 240:
            self.y = 240
            self.vel_y = 0
        if self.y <= 0:
            self.y = 0

    def draw(self):
        '''Draw the player on the screen'''
        print('jump', self.jump.active)
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
    
    def on_ground(self):
        return self.y >= 240
    
    def start_jump(self):
        if self.on_ground():
            # If we are on the ground, reset the jump
            # Give initial jump velocity
            self.jump.reset()
            self.vel_y = -MAX_MOVE
        elif self.vel_y < 0:
            self.jump.reactivate()
    
    def stop_jump(self):
        # deactivate the jump
        self.jump.deactivate()