from msilib.schema import Class
import pygame
from Maps import Maps
from Button import Button

class Display():
    def __init__(self, screen, helping, map=0):
        
        # get walls of map
        self.map_nr = map
        walls = Maps(self.map_nr).get_walls()
        
        # legned on the left
        self.total_width, self.total_height = screen.get_size()
        self.legend_surf = pygame.Surface((self.total_width/6, self.total_height))
        self.legend_rect =self.legend_surf.get_rect(topleft=(0,0))
        self.legend_surf.fill((64,64,64))
        # playable field on right
        self.arena_surf = pygame.Surface((self.total_width-self.total_width/6,self.total_height))
        self.arena_rect = self.arena_surf.get_rect(topleft=(self.total_width/6, 0))
        self.arena_surf.fill((56,74,12))
        # draw helping lines
        if helping:
            self.helping_blocks()
        
        # add walls to that arena
        if walls:
            for surf, rect in walls:
                self.arena_surf.blit(surf, rect)
        # and correct the x value for later collision check
        self.wall_rects = [rect[1].move(200,0) for rect in walls]

        # texts
        self.font = pygame.font.Font('font/Pixeltype.ttf', 50)
        self.score_text_surf = self.font.render('Score:', False, 'Black')
        self.score_text_rect = self.score_text_surf.get_rect(topleft = (self.total_width/60, self.total_height/20))
        self.time_surf = self.font.render('Time:', False, 'Black')
        self.time_rect = self.time_surf.get_rect(topleft = (self.total_width/60, self.total_height/6))

        # difficulty buttons
        self.easy_img = pygame.image.load('images/easy.png').convert_alpha()
        self.easy_button = Button(150, 480, self.easy_img, "", 100, 50)
        self.okay_img = pygame.image.load('images/okay.png').convert_alpha()
        self.okay_button = Button(280, 480, self.okay_img, "choose difficulty:", 100, 50, (205,205,0))
        self.hard_img = pygame.image.load('images/hard.png').convert_alpha()
        self.hard_button = Button(410, 480, self.hard_img, "", 100, 50)

        # start button
        self.start_img = pygame.image.load('images/start.png').convert_alpha()
        self.start_button = Button(950, 480, self.start_img, "", 200, 100)

        # map images & buttons
        self.map0_img = pygame.image.load('images/map0.png').convert_alpha()
        self.map0_button = Button(100, 150, self.map0_img, MAP_NAME(0).name)
        self.map1_img = pygame.image.load('images/map1.png').convert_alpha()
        self.map1_button = Button(450, 150, self.map1_img, MAP_NAME(1).name)
        self.map2_img = pygame.image.load('images/map2.png').convert_alpha()
        self.map2_button = Button(800, 150, self.map2_img, MAP_NAME(2).name)
        self.map3_img = pygame.image.load('images/map3.png').convert_alpha()
        self.map3_button = Button(100, 650, self.map3_img, MAP_NAME(3).name)
        self.map4_img = pygame.image.load('images/map4.png').convert_alpha()
        self.map4_button = Button(450, 650, self.map4_img, MAP_NAME(4).name)
        self.map5_img = pygame.image.load('images/map5.png').convert_alpha()
        self.map5_button = Button(800, 650, self.map5_img, MAP_NAME(5).name)


    def update(self, screen):
        '''funtion to display the defined elements
        
        args:
        
        screen -- surface to display on
        '''
        self.legend_surf.blit(self.score_text_surf, self.score_text_rect)
        self.legend_surf.blit(self.time_surf, self.time_rect)
        screen.blit(self.legend_surf, self.legend_rect)
        screen.blit(self.arena_surf, self.arena_rect)

    def time_score(self, screen, start_time, paused, paused_time):
        '''function to display the current time of the game
        
        args:
        screen -- surface to display time on
        start_time -- start time of pygame
        paused -- flag if game if pasued (time count shuld stop)
        
        return:
        
        current_time -- current time of the game in secs
        '''
        current_time = int(pygame.time.get_ticks()/ 1000) - start_time
        current_time -= paused_time
        if not paused:
            time_sec_surf = self.font.render(f'{current_time}', False, 'Black')
        else:
            time_sec_surf = self.font.render(f'PAUSED', False, 'Black')
        time_sec_rect = time_sec_surf.get_rect(topleft=(self.total_width/30, self.time_rect.bottom+20))
        screen.blit(time_sec_surf, time_sec_rect)
        print(current_time, paused_time)
        return current_time

    def score(self, screen, score):
        '''function to display the score (food eaten)
        
        args:
        
        screen -- surface to display score on
        score -- curretn score of the game
        '''
        score_surf = self.font.render(f'{score}', False, 'Black')
        score_rect = score_surf.get_rect(topleft=(40, self.score_text_rect.bottom+20))
        screen.blit(score_surf, score_rect)

    def start_screen(self, screen, score, time, flag, snake_speed):
        '''function to display message after game over
        
        args:
        
        screen -- surface to display messages on
        score -- endscore of game
        time -- time played in game
        flag -- true start screen/ false game-over screen
        snake_speed -- current speed of snake

        return:

        snake_speed -- speed of the snake
        '''

        # draw text
        if flag:
            # beginning
            screen.fill((128,128,0))
            welcome_surf = self.font.render('Welcome, please choose a map - press SPACE to start', False, 'Black')
            welcome_rect = welcome_surf.get_rect(center=(self.total_width/2, self.total_height/20))
            screen.blit(welcome_surf, welcome_rect)
        else:
            # game over
            screen.fill((64,64,64))
            score_message_surf = self.font.render(f'your score was: {score}  you played {time}  seconds', False, 'Green')
            score_message_rect = score_message_surf.get_rect(center=(self.total_width/2, self.total_height/20))
            screen.blit(score_message_surf, score_message_rect)

        # draw and react to buttons
        if self.map0_button.draw(screen):
            self.map_nr = 0
        if self.map1_button.draw(screen):
            self.map_nr = 1
        if self.map2_button.draw(screen):
            self.map_nr = 2
        if self.map3_button.draw(screen):
            self.map_nr = 3
        if self.map4_button.draw(screen):
            self.map_nr = 4
        if self.map5_button.draw(screen):
            self.map_nr = 5
        if self.easy_button.draw(screen):
            snake_speed = 150
        if self.okay_button.draw(screen):
            snake_speed = 100
        if self.hard_button.draw(screen):
            snake_speed = 50
        if self.start_button.draw(screen):
            # simulate a spacebar press to start game
            newevent = pygame.event.Event(pygame.KEYDOWN, unicode=" ", key=pygame.K_SPACE, mod=pygame.KMOD_NONE) #create the event
            pygame.event.post(newevent) #add the event to the queue

        map_text_surf = self.font.render(f'Your are playing   {MAP_NAME(self.map_nr).name}   next round on   {DIFF(snake_speed).name}!', False, 'Green')
        map_text_rect = map_text_surf.get_rect(center=(600,950))
        screen.blit(map_text_surf, map_text_rect)
        
        return snake_speed
    # #def start_screen(self, screen):
    #     '''function to display message before game start
        
    #     args:
        
    #     screen -- surface to display messages on
    #     '''
    #     # draw text
        # screen.fill((128,128,0))
        # welcome_surf = self.font.render('Welcome, please choose a map - press SPACE to start', False, 'Black')
        # welcome_rect = welcome_surf.get_rect(center=(self.total_width/2, self.total_height/20))
        # screen.blit(welcome_surf, welcome_rect)
    #     # draw and react to buttons

    #     if self.map0_button.draw(screen):
    #         self.map_nr = 0
    #     if self.map1_button.draw(screen):
    #         self.map_nr = 1
    #     if self.map2_button.draw(screen):
    #         self.map_nr = 2
    #     if self.map3_button.draw(screen):
    #         self.map_nr = 3
    #     if self.map4_button.draw(screen):
    #         self.map_nr = 4
    #     if self.map5_button.draw(screen):
    #         self.map_nr = 5
    #     if self.easy_button.draw(screen):
    #         print("easy")
    #     if self.okay_button.draw(screen):
    #         print("okay")
    #     if self.hard_button.draw(screen):
    #         print("hard")
    #     if self.start_button.draw(screen):
    #         # simulate a spacebar press to start game
    #         newevent = pygame.event.Event(pygame.KEYDOWN, unicode=" ", key=pygame.K_SPACE, mod=pygame.KMOD_NONE) #create the event
    #         pygame.event.post(newevent) #add the event to the queue

    #     map_text_surf = self.font.render(f'Your are playing   {MAP_NAME(self.map_nr).name}   next round!', False, 'Green')
    #     map_text_rect = map_text_surf.get_rect(center=(600,950))
    #     screen.blit(map_text_surf, map_text_rect)
        

    
    def helping_blocks(self):
        gras_color = (56,94,12)
        for row in range(50):
            if row % 2 == 0:
                for col in range(50):
                    if col % 2 == 0:
                        gras_rect = pygame.Rect(col*20,row*20,20,20)
                        pygame.draw.rect(self.arena_surf, gras_color, gras_rect)
            else:
                for col in range(50):
                    if col % 2 != 0:
                        gras_rect = pygame.Rect(col*20,row*20,20,20)
                        pygame.draw.rect(self.arena_surf, gras_color, gras_rect)

# enums for easyer printning/ handeling of names
from enum import Enum
class MAP_NAME(Enum):
    BASIC = 0
    PARCOUR = 1
    STAIRCAISE = 2
    BLOCK_OF_DOOM = 3
    CAGE = 4
    HALF = 5

class DIFF(Enum):
    EASY = 150
    OKAY = 100
    HARD = 50