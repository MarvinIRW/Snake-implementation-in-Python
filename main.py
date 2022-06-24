import pygame
from sys import exit # to savely close the game
from random import randint
from Player import Player
from Display import Display
from Food import Food

def pause():
    pause_start = int(pygame.time.get_ticks() / 1000) - start_time
    return pause_start

def unpause(time, pause_start):
    pause_duration = (int(pygame.time.get_ticks() / 1000) - start_time) - pause_start
    time += pause_duration
    return time

def initialization(map_selection, help_lines, snake_speed_local=100):
    # start of the game, important for seconds of each game
    global start_time
    start_time = int(pygame.time.get_ticks() / 1000)
    # score of one game
    global score
    score = 0
    # determine how fast the snake is (later for difficulty?)
    global snake_speed
    snake_speed = snake_speed_local
    # helping lines?
    global helping
    helping = help_lines
    # what map?
    global map
    map = map_selection
    # initialise the display
    global display
    display = Display(screen, helping, map)
    # player
    global player
    player = Player(display.arena_rect, snake_block)
    # food
    global food
    food = Food(screen, snake_block, player.player_pos, display.wall_rects)

    # move the player to approximately the middle 
    player.head_rect.update(720,500,player.head_rect.width, player.head_rect.height)
    player.x_change = 0
    player.y_change = 0

    # start the game
    global game_active
    game_active = True

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
# helping lines?
helping = True
# what map?
map = 5
# initialise the display
display = Display(screen, helping, map)
# player
player = Player(display.arena_rect, snake_block)
# food
food = Food(screen, snake_block, player.player_pos, display.wall_rects)




# timer for power ups
power_timer = pygame.USEREVENT + 1
pygame.time.set_timer(power_timer, 10000)
# timer for movement
move_timer = pygame.USEREVENT + 2
pygame.time.set_timer(move_timer, snake_speed)



while True:
    # this while loop shoulnd run faster than 60x per second (so max frame rate is 60)
    clock.tick(120)
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
            # check player input
            player.input()

            # movement timer
            if event.type == move_timer:
                # check if snake hit the food
                score = player.eat(food, score, display.wall_rects)
                # actually get the snake moving
                player.move()
                # check if the game is lost (doing it here cause just after movement one need to check the collision)
                game_active = player.collosion(display)

            # power up timer
            if event.type == power_timer:
                print("POOWER")

        # input for menu
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                initialization(map, helping)
    
    # active game
    if game_active:
        # draw elements and update everything
        display.update(screen)
        # add player
        player.draw(screen)
        # draw the food
        food.draw(screen)
        # display current time
        if not paused:
            time = display.time_score(screen, start_time)
        # display current score
        display.score(screen, score)
        x, y = pygame.mouse.get_pos()
        #print(x, y)
    # intro / outro menue
    else:
        if time == 0:
            display.start_screen(screen)
        else:
            display.end_screen(screen, score, time)
            
    # updates the screen(display surface)
    pygame.display.update()