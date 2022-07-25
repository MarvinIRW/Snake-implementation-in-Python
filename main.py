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
    time -= pause_duration
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
    pygame.time.set_timer(move_timer, snake_speed)
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
    player.player_pos[0].update(720,500,player.player_pos[0].width, player.player_pos[0].height)
    player.player_pos[1].update(720,520,player.player_pos[1].width, player.player_pos[1].height)
    player.x_change = 0
    player.y_change = -20

    # start the game
    global game_active
    game_active = True

# basically inistializes the pygame module
pygame.mixer.pre_init(44100,-16,2,512)
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
pause_time = 0
pause_time_total= 0
# score of one game
score = 0
# determine how fast the snake is (later for difficulty?)
snake_speed = 100
# helping lines?
helping = True
# initialise the display
display = Display(screen, helping)
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
            ##################pygame.event.wait()?
            paused = not paused
            if paused:
                pause_time = time
            else:
                pause_time = time - pause_time
                pause_time_total += pause_time                
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
                
                initialization(display.map_nr, helping, snake_speed_local=snake_speed)
    
    # active game
    if game_active:
        # draw elements and update everything
        display.update(screen)
        # add player
        player.draw(screen)
        # draw the food
        food.draw(screen)
        # display current time
        time = display.time_score(screen, start_time, paused, pause_time_total)
        # display current score
        display.score(screen, score)

        ################################################TESTING###################################
         
    # intro / outro menue

    # elif if paused:
    # some pause menu?
    else:
        if time == 0:
            snake_speed = display.start_screen(screen, score, time, True, snake_speed)

        else:
            snake_speed = display.start_screen(screen, score, time, False, snake_speed)
            
    # updates the screen(display surface)
    pygame.display.update()