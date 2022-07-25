import pygame
from random import randint

class Food():
    '''class to represent the food in the main game'''
    def __init__(self, screen, snake_size, body_rects, wall_rects):
        self.block_size = snake_size
        self.arena_width, self.arena_height = screen.get_size()
        self.food_surf = pygame.image.load('images/apple.png').convert_alpha()
        self.food_surf = pygame.transform.scale(self.food_surf, (snake_size, snake_size))
        #self.food_surf = pygame.Surface((snake_size,snake_size))
        self.x_corr = randint(10, 59)*20
        self.y_corr = randint(0,49)*20
        self.food_rect = self.food_surf.get_rect(topleft=(self.x_corr, self.y_corr))
        while(not self.food_legal(body_rects, wall_rects)):
            x_corr = randint(10, 59)*20
            y_corr = randint(0,49)*20
            self.food_rect.update(x_corr,y_corr, self.food_rect.width, self.food_rect.height)
        #self.food_surf.fill('Red')
        
    def food_legal(self, body_rects, wall_rects):
        if self.food_rect.collidelist(body_rects) >= 0 or self.food_rect.collidelist(wall_rects) >= 0:
            return False
        else:
            return True

    def move(self, body_rects, wall_rects):
        '''moves the food to a free spot on the map

        args:

        player_pos -- list of Rects of the snake positions
        arena_rect -- Rect of the arena
        '''
        '''moves the food to a free spot on the map'''
        x_corr = randint(10, 59)*20
        y_corr = randint(0,49)*20
        self.food_rect.update(x_corr,y_corr, self.food_rect.width, self.food_rect.height)
        # corr's cant touch the snake itself - food can't spawn inside snake
        while(not self.food_legal(body_rects, wall_rects)):
            x_corr = randint(10, 59)*20
            y_corr = randint(0,49)*20
            self.food_rect.update(x_corr,y_corr, self.food_rect.width, self.food_rect.height)


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


    def draw(self, screen):
        '''draws food on given surface'''
        screen.blit(self.food_surf, self.food_rect)

    