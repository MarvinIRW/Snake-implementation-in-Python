import pygame
class Maps():
    '''builds the different maps the player can choose from'''
    def __init__(self, map):
        # walls
        self.walls = []

        match map:
            case 1:
                self.build_1()
            case 2:
                self.build_2()
            case 3:
                self.build_3()
            case 4:
                self.build_4()
            case 5:
                self.build_5()


    def build_1(self):
        self.walls = []
        wall_surf = pygame.Surface((40,400))
        wall_rect = wall_surf.get_rect(topleft=(140, 80))
        wall_surf.fill('Orange')
        self.walls.append((wall_surf, wall_rect))
        wall_surf = pygame.Surface((160,20))
        wall_rect = wall_surf.get_rect(topleft=(260, 80))
        wall_surf.fill('Orange')
        self.walls.append((wall_surf, wall_rect))
        wall_surf = pygame.Surface((160,20))
        wall_rect = wall_surf.get_rect(topleft=(560, 80))
        wall_surf.fill('Orange')
        self.walls.append((wall_surf, wall_rect))
        wall_surf = pygame.Surface((300,20))
        wall_rect = wall_surf.get_rect(topleft=(560, 600))
        wall_surf.fill('Orange')
        self.walls.append((wall_surf, wall_rect))
        wall_surf = pygame.Surface((20,260))
        wall_rect = wall_surf.get_rect(topleft=(560, 80))
        wall_surf.fill('Orange')
        self.walls.append((wall_surf, wall_rect))
        wall_surf = pygame.Surface((160,20))
        wall_rect = wall_surf.get_rect(topleft=(200, 800))
        wall_surf.fill('Orange')
        self.walls.append((wall_surf, wall_rect))

    def build_2(self):
        self.walls = []
        for i in range(9):
            wall_surf = pygame.Surface((40,40))
            wall_rect = wall_surf.get_rect(topleft=(120*i, 120*i))
            wall_surf.fill('Orange')
            self.walls.append((wall_surf, wall_rect))

    def build_3(self):
        wall_surf = pygame.Surface((200,200))
        wall_rect = wall_surf.get_rect(topleft=(120, 120))
        wall_surf.fill('Orange')
        self.walls.append((wall_surf, wall_rect))
        wall_surf = pygame.Surface((200,200))
        wall_rect = wall_surf.get_rect(topright=(880, 120))
        wall_surf.fill('Orange')
        self.walls.append((wall_surf, wall_rect)) 
        wall_surf = pygame.Surface((200,200))
        wall_rect = wall_surf.get_rect(bottomleft=(120, 880))
        wall_surf.fill('Orange')
        self.walls.append((wall_surf, wall_rect)) 
        wall_surf = pygame.Surface((200,200))
        wall_rect = wall_surf.get_rect(bottomright=(880, 880))
        wall_surf.fill('Orange')
        self.walls.append((wall_surf, wall_rect)) 

    def build_4(self):
        wall_surf = pygame.Surface((600, 20))
        wall_rect = wall_surf.get_rect(topleft=(200, 200))
        wall_surf.fill('Orange')
        self.walls.append((wall_surf, wall_rect)) 
        wall_surf = pygame.Surface((600,20))
        wall_rect = wall_surf.get_rect(topleft=(200, 800))
        wall_surf.fill('Orange')
        self.walls.append((wall_surf, wall_rect)) 
        wall_surf = pygame.Surface((20,620))
        wall_rect = wall_surf.get_rect(topleft=(800, 200))
        wall_surf.fill('Orange')
        self.walls.append((wall_surf, wall_rect)) 
        wall_surf = pygame.Surface((20,280))
        wall_rect = wall_surf.get_rect(topleft=(200, 220))
        wall_surf.fill('Orange')
        self.walls.append((wall_surf, wall_rect)) 
        wall_surf = pygame.Surface((20,280))
        wall_rect = wall_surf.get_rect(topleft=(200, 520))
        wall_surf.fill('Orange')
        self.walls.append((wall_surf, wall_rect)) 

    def build_5(self):
        wall_surf = pygame.Surface((500,1000))
        wall_rect = wall_surf.get_rect(topleft=(0, 0))
        wall_surf.fill('Orange')
        self.walls.append((wall_surf, wall_rect)) 

    def get_walls(self):
        return self.walls