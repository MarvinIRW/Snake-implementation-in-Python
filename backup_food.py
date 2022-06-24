import pygame
from random import randint

class Food():
    '''class to represent the food in the main game'''
    def __init__(self, screen, snake_size):
        self.block_size = snake_size
        self.arena_width, self.arena_height = screen.get_size()
        self.food_surf = pygame.Surface((snake_size,snake_size))
        self.x_corr = randint(self.arena_width/120, ((self.arena_width/self.block_size)-1)*self.block_size)
        self.y_corr = randint(0, ((self.arena_width/self.block_size)-1)*self.block_size)
        self.food_rect = self.food_surf.get_rect(topleft=(self.x_corr, self.y_corr))
        self.food_surf.fill('Red')
        

    def move(self, player_pos, arena_rect):
        '''moves the food to a free spot on the map

        args:

        player_pos -- list of Rects of the snake positions
        arena_rect -- Rect of the arena
        '''
        self.new_random_pos()
        self.food_rect.update(self.x_corr, self.y_corr, self.food_rect.width, self.food_rect.height)
        
        #check if food is inside the snake
        while (self.food_rect.collidelist(player_pos) >= 0):
            self.new_random_pos()
            # update the food rect
            self.food_rect.update(self.x_corr, self.y_corr, self.food_rect.width, self.food_rect.height)
            
        print(self.x_corr, self.y_corr, "food corr")
        print(player_pos[0].topleft)


    def inside_snake(self, player_pos, arena_rect):
        '''helper function for move
        
        checks the nearby area around the snake for a legal position for the food
        '''
        x_test = self.x_corr - 3 * self.block_size
        y_test = self.y_corr - 3 * self.block_size
        for i in range():            
            for j in range(8):
                self.food_rect.update(x_test, y_test, self.food_rect.width, self.food_rect.height)
                # if now no collision and inside arena job is done
                if self.food_rect.collidelist(player_pos) == -1 and arena_rect.contains(self.food_rect):
                    self.x_corr = x_test
                    self.y_corr = y_test
                    return False
                x_test += self.block_size
            y_test += self.block_size
        # if area is still colliding
        return True

    def new_random_pos(self):
        '''creates a random pos on the arena (pos is equal to topleft pos of rect'''
        self.x_corr = randint(self.arena_width/120, ((self.arena_width/self.block_size)-1)*self.block_size)
        self.y_corr = randint(0, ((self.arena_width/self.block_size)-1)*self.block_size)

    def draw(self, screen):
        '''draws food on given surface'''
        screen.blit(self.food_surf, self.food_rect)

    