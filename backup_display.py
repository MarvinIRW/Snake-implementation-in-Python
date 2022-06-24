from msilib.schema import Class
import pygame

class Display():
    '''class to organize and to display the things needed for the game'''
    def __init__(self, screen, map):
        self.map = map
        # legned on the left
        self.total_width, self.total_height = screen.get_size()
        self.legend_surf = pygame.Surface((200, 1000))
        self.legend_rect =self.legend_surf.get_rect(topleft=(1000,0))
        self.legend_surf.fill((64,64,64))
        # playable field on right
        # self.arena_surf = pygame.Surface((self.total_width-self.total_width/6,self.total_height))
        # self.arena_rect = self.arena_surf.get_rect(topleft=(self.total_width/6, 0))
        # self.arena_surf.fill((150,150,150))
        # texts
        self.font = pygame.font.Font('font/Pixeltype.ttf', 50)
        self.score_text_surf = self.font.render('Score:', False, 'Black')
        self.score_text_rect = self.score_text_surf.get_rect(topleft = (self.total_width/60 + 1000, self.total_height/20))
        self.time_surf = self.font.render('Time:', False, 'Black')
        self.time_rect = self.time_surf.get_rect(topleft = (self.total_width/60 + 1000, self.total_height/6))
        self.legend_surf.blit(self.score_text_surf, self.score_text_rect)
        self.legend_surf.blit(self.time_surf, self.time_rect)
        
        

    def update(self, score, start_time, screen):
        '''funtion to display the defined elements
        
        args:
        
        screen -- surface to display on
        '''
        current_time = self.time_score(start_time, screen)
        self.score(score, screen)
        screen.blit(self.legend_surf, self.legend_rect)
        screen.blit(self.map.arena_surf, self.map.arena_rect)
        # screen.blit(self.arena_surf, self.arena_rect)
        #self.map.draw(self.screen)
        return current_time
        

    def time_score(self, start_time, screen):
        '''function to display the current time of the game
        
        args:

        screen -- surface to display time on
        start_time -- start time of pygame
        
        return:
        
        current_time -- current time of the game in secs
        '''
        current_time = int(pygame.time.get_ticks() / 1000) - start_time
        time_sec_surf = self.font.render(f'{current_time}', False, 'Black')
        time_sec_rect = time_sec_surf.get_rect(topleft=(self.total_width/30 + 1000, self.time_rect.bottom+20))
        screen.blit(time_sec_surf, time_sec_rect)
        return current_time

    def score(self, score, screen):
        '''function to display the score (food eaten)
        
        args:
        
        screen -- surface to display score on
        score -- curretn score of the game
        '''
        score_surf = self.font.render(f'{score}', False, 'Black')
        score_rect = score_surf.get_rect(topleft=(1040, self.score_text_rect.bottom+20))
        screen.blit(score_surf, score_rect)



    def end_screen(self, score, time, screen):
        '''function to display message after game over
        
        args:
        
        screen -- surface to display messages on
        score -- endscore of game
        time -- time played in game
        '''
        screen.fill((64,64,64))
        score_message_surf = self.font.render(f'your score was: {score}  you played {time}  seconds', False, 'Green')
        score_message_rect = score_message_surf.get_rect(center=(600,800))
        screen.blit(score_message_surf, score_message_rect)

    def start_screen(self, screen):
        '''function to display message before game start
        
        args:
        
        screen -- surface to display messages on
        '''
        screen.fill((64,64,64))
        welcome_surf = self.font.render('Welcome, please choose a map - press SPACE to start', False, 'Black')
        welcome_rect = welcome_surf.get_rect(center=(self.total_width/2, self.total_height/20))
        screen.blit(welcome_surf, welcome_rect)