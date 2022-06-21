import pygame
from sys import exit # to savely close the game
from random import randint
from Player import Player


def display_time_score():
    '''function to display the current time of the game'''
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    time_sec_surf = font.render(f'{current_time}', False, 'Black')
    time_sec_rect = time_sec_surf.get_rect(topleft=(40, time_rect.bottom+20))
    screen.blit(time_sec_surf, time_sec_rect)
    return current_time

def display_score():
    '''function to display the score (food eaten)'''
    score_surf = font.render(f'{score}', False, 'Black')
    score_rect = score_surf.get_rect(topleft=(40, score_text_rect.bottom+20))
    screen.blit(score_surf, score_rect)

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

# surfaces

# legned on the left
legend_surf = pygame.Surface((200,1000))
legend_rect = legend_surf.get_rect(topleft=(0,0))
legend_surf.fill((64,64,64))

# playable field on right
arena_surf = pygame.Surface((1000,1000))
arena_rect = arena_surf.get_rect(topleft=(200,0))
arena_surf.fill((150,150,150))

# # borders
# border_top_surf = pygame.Surface((1000,20))
# border_top_rect = border_top_surf.get_rect(topleft=(200,20))
# border_top_surf.fill('Gold')
# screen.blit(border_top_surf, border_top_rect)

# player
player = Player(arena_rect, snake_block)



# food
food_surf = pygame.Surface((snake_block,snake_block))
food_rect = food_surf.get_rect(topleft=(randint(10, 59)*20, randint(0,49)*20))
food_surf.fill('Red')



# texts
font = pygame.font.Font('font/Pixeltype.ttf', 50)

score_text_surf = font.render('Score:', False, 'Black')
score_text_rect = score_text_surf.get_rect(topleft = (20, legend_rect.top+50))

time_surf = font.render('Time:', False, 'Black')
time_rect = time_surf.get_rect(topleft = (20, legend_rect.top+150))

welcome_surf = font.render('Welcome, please choose a map - press SPACE to start', False, 'Black')
welcome_rect = welcome_surf.get_rect(center=(600,50))


# timer for power ups
power_timer = pygame.USEREVENT + 1
pygame.time.set_timer(power_timer, 10000)
# timer for movement
move_timer = pygame.USEREVENT + 2
pygame.time.set_timer(move_timer, snake_speed)



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
        
        # movement
        if game_active:
            player.input()

            # movement timer
            if event.type == move_timer:
                # actually get the snake moving
                player.move()
                # check if the game is lost (doing it here cause just after movement one need to check the collision)
                game_active = player.collosion(arena_rect)
                

            # power up timer
            if event.type == power_timer:
                print("test")
            
        # input for menu
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # reset snake position
                player.head_rect.update(720,500,player.head_rect.width, player.head_rect.height)
                game_active = True
                
                # needed to reset the time score of the game
                start_time = int(pygame.time.get_ticks() / 1000)
    
    # active game
    if game_active:
        # draw elements and update everything
        legend_surf.blit(score_text_surf, score_text_rect)
        legend_surf.blit(time_surf, time_rect)
        screen.blit(legend_surf,legend_rect)
        screen.blit(arena_surf, arena_rect)
        # add player
        player.draw(screen)

        screen.blit(food_surf, food_rect)
        time = display_time_score()
        display_score()

        
        # check if snake hit the food
        if food_rect.colliderect(player.head_rect):
            score += 1
            player.create_bodypart(food_rect)
            move_food(player.head_rect)

    # intro menue
    else:
        screen.fill((64,64,64))
        score_message_surf = font.render(f'your score was: {score}  you played {time}  seconds', False, 'Green')
        score_message_rect = score_message_surf.get_rect(center=(600,800))

        if time == 0:
            screen.blit(welcome_surf, welcome_rect)
        else:
            screen.blit(score_message_surf, score_message_rect)
            
    # updates the screen(display surface)
    pygame.display.update()

