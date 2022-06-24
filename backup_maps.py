import pygame
class Maps():
    '''builds the different maps the player can choose from'''
    def __init__(self, screen):
        # playable area
        self.total_width, self.total_height = screen.get_size()
        self.arena_surf = pygame.Surface((self.total_width-self.total_width/6,self.total_height))
        self.arena_rect = self.arena_surf.get_rect(topleft=(0, 0))
        self.arena_surf.fill((150,150,150))
        # walls
        self.walls = []

    def build_1(self):
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
        wall_surf = pygame.Surface((20,250))
        wall_rect = wall_surf.get_rect(topleft=(560, 80))
        wall_surf.fill('Orange')
        self.walls.append((wall_surf, wall_rect))
        wall_surf = pygame.Surface((160,20))
        wall_rect = wall_surf.get_rect(topleft=(200, 800))
        wall_surf.fill('Orange')
        self.walls.append((wall_surf, wall_rect))

    def draw(self, screen):
        for surf, rect in self.walls:
            self.arena_surf.blit(surf, rect)
        screen.blit(self.arena_surf, self.arena_rect)