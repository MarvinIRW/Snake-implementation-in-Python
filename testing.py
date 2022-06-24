import pygame
from Maps import Maps
# Window size
window_x = 1000
window_y = 1000

# Initialising pygame
pygame.init()
clock = pygame.time.Clock()
# Initialise game window
pygame.display.set_caption('GeeksforGeeks Snakes')
screen = pygame.display.set_mode((window_x, window_y))

for i in range(50):

    pygame.draw.line(screen, 'White', (i*20, 0), (i*20, 1000))
    pygame.draw.line(screen, 'White', (0, i*20), (1000, i*20))

walls = []

wall_surf = pygame.Surface((40,400))
wall_rect = wall_surf.get_rect(topleft=(140, 80))
wall_surf.fill('Orange')
walls.append((wall_surf, wall_rect))
wall_surf = pygame.Surface((160,20))
wall_rect = wall_surf.get_rect(topleft=(260, 80))
wall_surf.fill('Orange')
walls.append((wall_surf, wall_rect))
wall_surf = pygame.Surface((160,20))
wall_rect = wall_surf.get_rect(topleft=(560, 80))
wall_surf.fill('Orange')
walls.append((wall_surf, wall_rect))
wall_surf = pygame.Surface((300,20))
wall_rect = wall_surf.get_rect(topleft=(560, 600))
wall_surf.fill('Orange')
walls.append((wall_surf, wall_rect))
wall_surf = pygame.Surface((20,250))
wall_rect = wall_surf.get_rect(topleft=(560, 80))
wall_surf.fill('Orange')
walls.append((wall_surf, wall_rect))
wall_surf = pygame.Surface((160,20))
wall_rect = wall_surf.get_rect(topleft=(200, 800))
wall_surf.fill('Orange')
walls.append((wall_surf, wall_rect))


while True:
     # this while loop shoulnd run faster than 60x per second (so max frame rate is 60)
    clock.tick(1)
    # event loop
    for event in pygame.event.get():
        # so one can close the window with x-button
        if event.type == pygame.QUIT:
            
            # kinda the opposit of pygame.init()
            pygame.quit()
            # close the code savely
            exit()
    
    for surf, rect in walls:
        screen.blit(surf, rect)

    x, y = pygame.mouse.get_pos()
    print(x, y)
    
    pygame.display.update()
