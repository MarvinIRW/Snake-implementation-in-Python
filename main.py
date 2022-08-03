# Imports for running the game
import pygame
from sys import exit # to safely close the game
from Player import Player
from Display import Display
from Food import Food
from PowerUp import PowerUp

# basically initializes the pygame module
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
# determine how fast the snake is (corresponds to ms interval the snake moves)
snake_speed = 100
effected_speed = 0
# helping lines?
helping = True
# initialize the display
display = Display(screen, helping)
# player
player = Player(display.arena_rect, snake_block)
# food
food = Food(screen, snake_block, player.player_pos, display.wall_rects)
# powerup
power_up = PowerUp(snake_block)
power_on = False
power_took = False

# timer for power ups popping up
power_appear_timer = pygame.USEREVENT + 1
pygame.time.set_timer(power_appear_timer, 15000)
# timer for movement
move_timer = pygame.USEREVENT + 2
pygame.time.set_timer(move_timer, snake_speed)

# how long should power up last
power_lasting_timer = pygame.USEREVENT + 3
pygame.time.set_timer(power_lasting_timer, 3000)

def initialization(map_selection, help_lines, snake_speed_local=100):
    '''method to reset all important variables for the game
    
    args:
    
    map_selection -- int corresponding to the chosen map
    help_lines -- if the Check pattern should be drawn (player selection not implemented)
    snake_speed_local -- the chosen difficulty'''
    # start of the game, important for seconds of each game
    global start_time
    start_time = int(pygame.time.get_ticks() / 1000)
    global pause_time_total
    pause_time_total= 0
    # score of one game
    global score
    score = 0
    # determine how fast the snake is
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
    # initialize the display
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
    # power up could not exist
    try:
        power_up
    except NameError:
        del power_up    
    global power_on
    power_on = False
    power_took = False

    # move the player to approximately the middle 
    player.player_pos[0].update(720,500,player.player_pos[0].width, player.player_pos[0].height)
    player.player_pos[1].update(720,520,player.player_pos[1].width, player.player_pos[1].height)
    # set snake direction
    player.x_change = 0
    player.y_change = -20

    # start the game
    global game_active
    game_active = True

# main loop
while True:
    # this while loop should not run faster 120x per second (so max frame rate is 120)
    clock.tick(120)
    # event loop
    for event in pygame.event.get():
        # so one can close the window with x-button
        if event.type == pygame.QUIT:
            # kind of the opposite of pygame.init()
            pygame.quit()
            # close the code safely
            exit()
        # 'x' closes the game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            pygame.quit()
            exit()

        # game paused?
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            paused = not paused
            # pause the game
            if paused:
                pause_time = time
            # unpause the game and add paused time to pause_time_total
            else:
                pause_time = time - pause_time
                pause_time_total += pause_time                
        # movement, power up spawn
        if game_active and not paused:
            # check player input
            player.input()

            # movement timer
            if event.type == move_timer:
                # check if snake hit the food
                score = food.eaten(player, score, display.wall_rects)
                # check if snake hit powerup
                if power_on:
                    power_on, power_took = power_up.snake_on_power(player.player_pos[0], snake_speed, move_timer, power_lasting_timer, power_appear_timer)
                # actually get the snake moving
                player.move()
                # check if the game is lost (doing it here cause just after movement one need to check the collision)
                game_active = player.collosion(display)

            # if timer for power up duarion is over:
            if event.type == power_lasting_timer and power_took:
                # set effected speed back to 0
                effected_speed = 0
                # and adjust snake speed 
                pygame.time.set_timer(move_timer, snake_speed)
                print("reset speed")
                power_took = False

            # power up timer adds a powerup to playing field and
            # relocates it if not picked up
            if event.type == power_appear_timer:
                power_on = not power_on
                if power_on:
                    power_up = PowerUp(snake_block)
                    power_up.deploy(player.player_pos, display.wall_rects, food.food_rect)

        # input for menu
        else:
            # if new game is started
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
        # draw the power up if there is one
        if power_on:
            power_up.draw(screen)
        # display current time
        time = display.time_score(screen, start_time, paused, pause_time_total)
        # display current score
        display.score(screen, score)

    # if not in active game draw the start or end screen
    else:
        # start screen
        if time == 0:
            snake_speed = display.start_screen(screen, score, time, True, snake_speed)
        # end screen
        else:
            snake_speed = display.start_screen(screen, score, time, False, snake_speed)
            
    # updates the screen(display surface)
    pygame.display.update()

