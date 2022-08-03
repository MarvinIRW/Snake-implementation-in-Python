import pygame
from random import randint

class PowerUp():
    '''class to represent the power-ups in the main game'''
    def __init__(self, snake_size):
        '''constructor of the PowerUp class
        
        snake_size -- size of on snake block'''
        # get random power effect
        self.power = POWER_EFFECT(randint(0,1))
        self.block_size = snake_size
        # assign image depending on power effect
        if self.power == POWER_EFFECT.SLOW:
            self.power_surf = pygame.image.load('images/sleep.png').convert_alpha()
            self.power_surf = pygame.transform.scale(self.power_surf, (snake_size, snake_size))
            self.sound = pygame.mixer.Sound('sound/slow.wav')

        elif self.power == POWER_EFFECT.FAST:
            self.power_surf = pygame.image.load('images/speed.png').convert_alpha()
            self.power_surf = pygame.transform.scale(self.power_surf, (snake_size, snake_size))
            self.sound = pygame.mixer.Sound('sound/fast.wav')
        self.power_rect = self.power_surf.get_rect()
        
    def power_legal(self, body_rects, wall_rects, food_rect):
        '''checks if the power up is in a legal position
        
        args:
        
        body_rects -- rects of the snake
        wall_rects -- rects of the walls
        food_rect -- rect of the food
        '''
        if self.power_rect.collidelist(body_rects) >= 0 or self.power_rect.collidelist(wall_rects) >= 0 or self.power_rect.colliderect(food_rect):
            return False
        else:
            return True

    def deploy(self, body_rects, wall_rects, food_rect):
        '''deploys a power up on the map

        args:

        player_pos -- list of Rects of the snake positions
        arena_rect -- Rect of the arena
        food_rect -- Rect of the food
        '''
        # get random position in arena
        x_corr = randint(10, 59)*20
        y_corr = randint(0,49)*20
        self.power_rect.update(x_corr,y_corr, self.power_rect.width, self.power_rect.height)
        # corr's cant touch the snake itself - powerup can't spawn inside snake
        while(not self.power_legal(body_rects, wall_rects, food_rect)):
            x_corr = randint(10, 59)*20
            y_corr = randint(0,49)*20
            self.power_rect.update(x_corr,y_corr, self.power_rect.width, self.power_rect.height)

    def snake_on_power(self, head, snake_speed, move_timer, power_lasting_timer, power_appear_timer):
        '''checks if snake hit the powerup and calls the right method for the effect
        
        args:
        
        head -- head of the snake
        snake_speed -- speed of snake in main game (corresponds to ms interval the snake moves)
        move_timer -- timer snake_speed is used in
        power_lasting_timer -- timer how long the power up effect should last
        power_apper_tiemr -- timer when the next power up should appear

        
        returns:
        
        power_on -- flag in main game to display power-up
        power_took -- flag for power up taking
        '''
        # if power up is picked up
        if self.power_rect.colliderect(head):
            if self.power == POWER_EFFECT.SLOW:
                self.power_slow(snake_speed, move_timer, power_lasting_timer, power_appear_timer)
                self.play_sound()
                return False, True
            elif self.power.value == POWER_EFFECT.FAST.value:
                self.power_fast(snake_speed, move_timer, power_lasting_timer, power_appear_timer)
                self.play_sound()
                return False, True
        # if not
        return True, False

    def power_slow(self, snake_speed, move_timer, power_lasting_timer, power_appear_timer):
        '''sets appropriate timers for the slowdown of the snake'''
        pygame.time.set_timer(move_timer, int(snake_speed*2))
        # how long should power up last
        pygame.time.set_timer(power_lasting_timer, 3000)
        # next power up should accur in sec
        pygame.time.set_timer(power_appear_timer, 15000)

    def power_fast(self, snake_speed, move_timer, power_lasting_timer, power_appear_timer):
        '''sets appropriate timers for the speedup of the snake'''
        pygame.time.set_timer(move_timer, int(snake_speed/2))
        # how long should power up last
        pygame.time.set_timer(power_lasting_timer, 3000)
        # next power up should accur in sec
        pygame.time.set_timer(power_appear_timer, 15000)


    def play_sound(self):
            '''plays a sound corresponding to the power up'''
            self.sound.play()
    

    def draw(self, screen):
        '''draws food on given surface'''
        screen.blit(self.power_surf, self.power_rect)

# enum for the different effects
# could be extended in future 
from enum import Enum
class POWER_EFFECT(Enum):
    SLOW = 0
    FAST = 1

    