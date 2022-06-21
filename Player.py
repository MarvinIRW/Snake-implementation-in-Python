import pygame


class Player():
    def __init__(self, arena_rect, snake_size):
        super().__init__()
        # for now just a surface, later maybe an actual image
        # head looks different than body
        self.head_img = pygame.Surface((snake_size,snake_size))
        self.head_img.fill('Yellow')
        self.head_rect = self.head_img.get_rect(topleft=arena_rect.center)

        # looks for body
        self.body_img = pygame.Surface((snake_size,snake_size))
        self.body_img.fill('Black')

        # list with all the rects of the player (head always on index 0)
        self.player_pos = []
        self.player_pos.append(self.head_rect)

        # movement variabels
        self.x_change = 0
        self.y_change = 0

    def input(self):
        '''function to monitor if the gamer did inputs relevant for the player'''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.x_change = 0
            self.y_change = -20
        if keys[pygame.K_DOWN]:
            self.x_change = 0
            self.y_change = 20
        if keys[pygame.K_LEFT]:
            self.x_change = -20
            self.y_change = 0
        if keys[pygame.K_RIGHT]:
            self.x_change = 20
            self.y_change = 0

    def create_bodypart(self, food_rect):
        '''adds another body part to the snake depending on the position of the just eaten food.

            args:

            food_rect -- Rect of the food just collected (important to get the position of the new bodypart)
            '''
    
        # get corr of the food
        x_corr = food_rect.center[0]
        y_corr = food_rect.center[1]
        # and add it to body list
        self.player_pos.append(self.body_img.get_rect(center=(x_corr, y_corr)))

    def move(self):
        '''moves the whole snake further depending on the direction'''
        last_x = self.player_pos[0].x
        last_y = self.player_pos[0].y
        # head get's moved in moving direction
        self.player_pos[0].x += self.x_change
        self.player_pos[0].y += self.y_change
        for body in self.player_pos[1:]:
            # other parts get pushed to pos of body in front
            temp_x = body.x
            temp_y = body.y
            body.x = last_x
            body.y = last_y
            last_x = temp_x
            last_y = temp_y
        

    def collosion(self, arena_rect):
        '''checks if the player is still in bounds of arena and is not hitting it's own body
        
        args:
        
        arena_rect -- Rect of the arena played in
        
        returns:

        bool if the gamestate is still active or not'''
        game_active = True
        # snake outside the arena?
        if (not arena_rect.contains(self.head_rect)):
            game_active = False
        # snake touching itself?
        for body in self.player_pos[1:]:
            if self.head_rect.center == body.center:
                game_active = False
        return game_active

    def draw(self, screen):
        '''draws the whole player on the screen
        
        args:
        
        screen -- surface (where the player should be drawn on)'''
        
        screen.blit(self.head_img, self.head_rect)
        # and rest of body
        for body in self.player_pos[1:]:
            screen.blit(self.body_img,body)