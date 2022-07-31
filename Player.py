import pygame


class Player():
    '''Class representing the snake'''
    def __init__(self, arena_rect, snake_size):
        '''constructor for Player class
        
        args:
        
        arena_rect -- rect of the playable surface
        snake_size -- size of on snake block'''
        # head looks different than body
        self.head_img = pygame.Surface((snake_size,snake_size))
        self.head_img.fill('Yellow')
        # looks for body
        self.body_img = pygame.Surface((snake_size,snake_size))
        self.body_img.fill('Black')
        # list with all the rects of the player (head always on index 0) starting with two parts
        self.player_pos = []
        self.player_pos.append(self.head_img.get_rect(topleft=arena_rect.center))
        self.player_pos.append(self.body_img.get_rect(topleft=(arena_rect.center)))
        self.player_pos[0].update(720,500,self.player_pos[0].width, self.player_pos[0].height)
        self.player_pos[1].update(720,520,self.player_pos[1].width, self.player_pos[1].height)
        # movement variabels
        self.x_change = 0
        self.y_change = -20
        # snake images and resizing
        self.head_up = pygame.image.load('images/head_up.png').convert_alpha()
        self.head_up = pygame.transform.scale(self.head_up, (snake_size, snake_size))
        self.head_down = pygame.image.load('images/head_down.png').convert_alpha()
        self.head_down = pygame.transform.scale(self.head_down, (snake_size, snake_size))
        self.head_right = pygame.image.load('images/head_right.png').convert_alpha()
        self.head_right = pygame.transform.scale(self.head_right, (snake_size, snake_size))
        self.head_left = pygame.image.load('images/head_left.png').convert_alpha()
        self.head_left = pygame.transform.scale(self.head_left, (snake_size, snake_size))

        self.tail_up = pygame.image.load('images/tail_up.png').convert_alpha()
        self.tail_up = pygame.transform.scale(self.tail_up, (snake_size, snake_size))
        self.tail_down = pygame.image.load('images/tail_down.png').convert_alpha()
        self.tail_down = pygame.transform.scale(self.tail_down, (snake_size, snake_size))
        self.tail_right = pygame.image.load('images/tail_right.png').convert_alpha()
        self.tail_right = pygame.transform.scale(self.tail_right, (snake_size, snake_size))
        self.tail_left = pygame.image.load('images/tail_left.png').convert_alpha()
        self.tail_left = pygame.transform.scale(self.tail_left, (snake_size, snake_size))

        self.body_vertical = pygame.image.load('images/body_vertical.png').convert_alpha()
        self.body_vertical = pygame.transform.scale(self.body_vertical, (snake_size, snake_size))
        self.body_horizontal = pygame.image.load('images/body_horizontal.png').convert_alpha()
        self.body_horizontal = pygame.transform.scale(self.body_horizontal, (snake_size, snake_size))

        self.body_tr = pygame.image.load('images/body_topright.png').convert_alpha()
        self.body_tr = pygame.transform.scale(self.body_tr, (snake_size, snake_size))
        self.body_tl = pygame.image.load('images/body_topleft.png').convert_alpha()
        self.body_tl = pygame.transform.scale(self.body_tl, (snake_size, snake_size))
        self.body_br = pygame.image.load('images/body_bottomright.png').convert_alpha()
        self.body_br = pygame.transform.scale(self.body_br, (snake_size, snake_size))
        self.body_bl = pygame.image.load('images/body_bottomleft.png').convert_alpha()
        self.body_bl = pygame.transform.scale(self.body_bl, (snake_size, snake_size))

    def input(self):
        '''function to monitor if the gamer did inputs relevant for the player'''
        keys = pygame.key.get_pressed()
        # move up
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            # cant move in opposit direction
            if self.y_change != 20:
                self.x_change = 0
                self.y_change = -20
        # move down
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            # cant move in opposit direction
            if self.y_change != -20:
                self.x_change = 0
                self.y_change = 20
        # move left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.x_change != 20:
                self.x_change = -20
                self.y_change = 0
        # move right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.x_change != -20:
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
        # helper variabels
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
        
    def collosion(self, display):
        '''checks if the player is still in bounds of arena and is not hitting it's own body
        
        args:
        
        display -- object from class Display
        
        returns:
        game_active -- bool if the gamestate is still active or not'''
        game_active = True
        # snake outside the arena?
        if (not display.arena_rect.contains(self.player_pos[0])):
            game_active = False
        # snake touching itself?
        for body in self.player_pos[1:]:
            if self.player_pos[0].center == body.center:
                game_active = False
                #print("chrashed in body.")
        # snake touching walls?
        index = self.player_pos[0].collidelist(display.wall_rects)
        if index >= 0:
            #print(display.wall_rects[index], "PLayer pos: " , self.player_pos[0])
            game_active = False
            #print("crashed in wall")
        return game_active
        
    def draw(self, screen):
        '''draws the whole player on the screen
        
        args:
        
        screen -- surface (where the player should be drawn on)'''
        #helper functions for head and body
        self.update_head_image()
        self.update_tail_image()
        for index, part in enumerate(self.player_pos):
            # what direction is head heading?
            if index == 0:
                screen.blit(self.head_curr,part)
            # tail
            elif index == len(self.player_pos) - 1:
                screen.blit(self.tail_curr,part)
            else:
                previous_block_x = self.player_pos[index + 1].x - part.x
                previous_block_y = self.player_pos[index + 1].y - part.y
                next_block_x = self.player_pos[index - 1].x - part.x
                next_block_y = self.player_pos[index - 1].y - part.y
                if previous_block_x == next_block_x:
                    # vertical block
                    screen.blit(self.body_vertical, part)
                elif previous_block_y == next_block_y:
                    # horizontal block
                    screen.blit(self.body_horizontal, part)
                else:
                    # corners
                    if previous_block_x == -20 and next_block_y == -20 or previous_block_y == -20 and next_block_x == -20:
                        screen.blit(self.body_tl, part)
                    elif previous_block_x == -20 and next_block_y == 20 or previous_block_y == 20 and next_block_x == -20:
                        screen.blit(self.body_bl, part)
                    elif previous_block_x == 20 and next_block_y == -20 or previous_block_y == -20 and next_block_x == 20:
                        screen.blit(self.body_tr, part)
                    elif previous_block_x == 20 and next_block_y == 20 or previous_block_y == 20 and next_block_x == 20:
                        screen.blit(self.body_br, part)

    def update_tail_image(self):
        '''selects the appropriate tail images depending on the current movement'''
        x = self.player_pos[-2].x - self.player_pos[-1].x
        y = self.player_pos[-2].y - self.player_pos[-1].y
        # left
        if (x == 20 and y == 0): self.tail_curr = self.tail_left
        # right
        elif (x == -20 and y == 0): self.tail_curr = self.tail_right
        # up
        elif (x == 0 and y == 20): self.tail_curr = self.tail_up
        # down
        elif (x == 0 and y == -20): self.tail_curr = self.tail_down

    def update_head_image(self):

        '''selects the appropriate head images depending on the current movement'''
        x = self.player_pos[1].x - self.player_pos[0].x
        y = self.player_pos[1].y - self.player_pos[0].y
        # left
        if (x == 20 and y == 0): self.head_curr = self.head_left
        # right
        elif (x == -20 and y == 0): self.head_curr = self.head_right
        # up
        elif (x == 0 and y == 20): self.head_curr = self.head_up
        # down
        elif (x == 0 and y == -20): self.head_curr = self.head_down