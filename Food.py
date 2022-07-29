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
        self.crunch_sound = pygame.mixer.Sound('sound/crunch.wav')
        
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
        x_corr = randint(10, 59)*20
        y_corr = randint(0,49)*20
        self.food_rect.update(x_corr,y_corr, self.food_rect.width, self.food_rect.height)
        # corr's cant touch the snake itself - food can't spawn inside snake
        while(not self.food_legal(body_rects, wall_rects)):
            x_corr = randint(10, 59)*20
            y_corr = randint(0,49)*20
            self.food_rect.update(x_corr,y_corr, self.food_rect.width, self.food_rect.height)

    def eaten(self, player, score, wall_rects):
        '''checks if player is on food if so increases score makes a new bodypart and moves the food
        
        args:
        
        player -- instance of class Player
        score -- score of the game
        wall_rects -- list of wall rects in arena
        '''

        if self.food_rect.colliderect(player.player_pos[0]):
            score += 1
            player.create_bodypart(self.food_rect)
            self.move(player.player_pos, wall_rects)
            self.play_curnchy()
            return score
        return score
    
    def draw(self, screen):
        '''draws food on given surface'''
        screen.blit(self.food_surf, self.food_rect)

    def play_curnchy(self):
        '''plays a cunshing sound'''
        self.crunch_sound.play()

    