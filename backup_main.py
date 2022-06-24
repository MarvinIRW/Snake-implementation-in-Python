import pygame
from sys import exit # to savely close the game
from random import randint
from Player import Player
from Display import Display
from Maps import Maps

def pause():
    pause_start = int(pygame.time.get_ticks() / 1000) - start_time
    return pause_start

def unpause(time, pause_start):
    pause_duration = (int(pygame.time.get_ticks() / 1000) - start_time) - pause_start
    time += pause_duration
    return time

def move_food(head_rect):
    '''moves the food to a free spot on the map'''
    x_corr = randint(10, 59)*20
    y_corr = randint(0,49)*20
    # corr's cant touch the snake itself - food can't spawn inside snake
    while(head_rect.collidepoint(x_corr, y_corr)):
        x_corr = randint(10, 59)*20
        y_corr = randint(0,49)*20
    food_rect.update(x_corr,y_corr,food_rect.width, food_rect.height)

# basically inistializes the pygame module
pygame.init()
# display surface
screen = pygame.display.set_mode((1200,1000))
# name the display windows caption
pygame.display.set_caption("Snake")
# set a new icon for the window
pygame.display.set_icon(pygame.image.load('images/Snake-icon.png'))
# clock object to help with time related stuff e.g. timer and frame rates
clock = pygame.time.Clock()
# game state
game_active = False
# pause state
paused = False
# holds the snake size
snake_block = 20
# start of the game, important for seconds of each game
start_time = 0
# actual seconds of one instance of a game
time = 0
# score of one game
score = 0
# determine how fast the snake is (later for difficulty?)
snake_speed = 100


# TESTING********************************************************************+
arena = Maps(screen)
arena.build_1()

# initialise the display
display = Display(screen, arena)

# # borders
# border_top_surf = pygame.Surface((1000,20))
# border_top_rect = border_top_surf.get_rect(topleft=(200,20))
# border_top_surf.fill('Gold')
# screen.blit(border_top_surf, border_top_rect)

# player
player = Player(arena.arena_rect, snake_block)



# food
food_surf = pygame.Surface((snake_block,snake_block))
food_rect = food_surf.get_rect(topleft=(randint(10, 59)*20, randint(0,49)*20))
food_surf.fill('Red')

# timer for power ups
power_timer = pygame.USEREVENT + 1
pygame.time.set_timer(power_timer, 10000)
# timer for movement
move_timer = pygame.USEREVENT + 2
pygame.time.set_timer(move_timer, snake_speed)

# TESTING
for i in range(50):

    pygame.draw.line(arena.arena_surf, 'White', (i*20, 0), (i*20, 1000))
    pygame.draw.line(arena.arena_surf, 'White', (0, i*20), (1000, i*20))

while True:
    # this while loop shoulnd run faster than 60x per second (so max frame rate is 60)
    clock.tick(60)


    # event loop
    for event in pygame.event.get():
        # so one can close the window with x-button
        if event.type == pygame.QUIT:
            
            # kinda the opposit of pygame.init()
            pygame.quit()
            # close the code savely
            exit()
        # 'x' closes the game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            pygame.quit()
            exit()

        # game pasued?
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            paused = not paused
            if paused:
                pause_start = pause()
            else:
                time = unpause(time, pause_start)
        # movement
        if game_active and not paused:
            player.input()

            # movement timer
            if event.type == move_timer:
                # actually get the snake moving
                player.move()
                # check if the game is lost (doing it here cause just after movement one need to check the collision)
                game_active = player.collosion(arena.arena_rect, arena.walls)

            # power up timer
            if event.type == power_timer:
                print("test")

        # input for menu
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # reset snake position
                player.head_rect.update(720,500,player.head_rect.width, player.head_rect.height)
                # needed to reset the time score of the game
                start_time = int(pygame.time.get_ticks() / 1000)
                game_active = True
    
    # active game
    if game_active:
        # add player
        player.draw(arena.arena_surf)
        # draw elements and update everything
        time = display.update(score, start_time, screen)
        # draw the food
        arena.arena_surf.blit(food_surf, food_rect)
        # draw arena
        arena.draw(screen)

        # check if snake hit the food
        if food_rect.colliderect(player.head_rect):
            score += 1
            player.create_bodypart(food_rect)
            print("yummy")
            move_food(player.head_rect)
    # intro / outro menue
    else:
        if time == 0:
            display.start_screen(screen)
        else:
            #print("head rect: ", player.head_rect)
            display.end_screen(score, time, screen)
            
    # updates the screen(display surface)
    pygame.display.update()