from contextlib import nullcontext
from time import process_time_ns
import pygame
from sys import exit # to savely close the game
from random import randint
from Player import Player
from Display import Display
from Food import Food
from PowerUp import PowerUp


def initialization(map_selection, help_lines, snake_speed_local=100):
    # start of the game, important for seconds of each game
    global start_time
    start_time = int(pygame.time.get_ticks() / 1000)
    global pause_time_total
    pause_time_total= 0
    # score of one game
    global score
    score = 0
    # determine how fast the snake is (later for difficulty?)
    global snake_speed
    snake_speed = snake_speed_local
    pygame.time.set_timer(move_timer, snake_speed)
    # reset power up timer
    pygame.time.set_timer(power_appear_timer, 15000)
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
    # power up
    global power_up
    del power_up
    global power_on
    power_on = False



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
effected_speed = 0
# helping lines?
helping = True
# initialise the display
display = Display(screen, helping)
# player
player = Player(display.arena_rect, snake_block)
# food
food = Food(screen, snake_block, player.player_pos, display.wall_rects)
# powerup
power_up = PowerUp(snake_block)
power_on = False





# timer for power ups popping up
power_appear_timer = pygame.USEREVENT + 1
pygame.time.set_timer(power_appear_timer, 15000)
# timer for movement
move_timer = pygame.USEREVENT + 2
pygame.time.set_timer(move_timer, snake_speed)

# how long should power up last
power_lasting_timer = pygame.USEREVENT + 3
pygame.time.set_timer(power_lasting_timer, 3000)



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
            # pause the game
            if paused:
                pause_time = time
            # unpause the game and add paused time to pause_time_total
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
                #score = player.eat(food, score, display.wall_rects)
                score = food.eaten(player, score, display.wall_rects)
                # check if snake hit powerup
                if power_on:
                    power_on = power_up.snake_on_power(player.player_pos[0], snake_speed, move_timer, power_lasting_timer, power_appear_timer)
                # actually get the snake moving
                player.move()
                # check if the game is lost (doing it here cause just after movement one need to check the collision)
                game_active = player.collosion(display)

            # if timer for power up duarion is over:
            if event.type == power_lasting_timer:
                # set effected speed back to 0
                effected_speed = 0
                # and adjust snake speed 
                pygame.time.set_timer(move_timer, snake_speed)
                print("reset speed")

            # power up timer adds a powerup to playingfield and
            # relocates it if not picked up
            if event.type == power_appear_timer:
                power_on = not power_on
                if power_on:
                    power_up = PowerUp(snake_block)
                    power_up.deploy(player.player_pos, display.wall_rects, food.food_rect)
                
                

                

        # input for menu
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # resets all important parameters
                initialization(display.map_nr, helping, snake_speed_local=snake_speed)
    
    # active game
    if game_active:
        # draw elements and update everything
        display.update(screen)
        # add player
        player.draw(screen)
        # draw the food
        food.draw(screen)
        # draw the power up
        if power_on:
            power_up.draw(screen)
        # display current time
        time = display.time_score(screen, start_time, paused, pause_time_total)
        # display current score
        display.score(screen, score)

    # if not in active game draw the start and end screen
    else:
        # start screen
        if time == 0:
            snake_speed = display.start_screen(screen, score, time, True, snake_speed)
        # end screen
        else:
            snake_speed = display.start_screen(screen, score, time, False, snake_speed)
            
    # updates the screen(display surface)
    pygame.display.update()