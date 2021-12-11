import random
import sys
import pygame
from pygame.locals import *

# Global Variable fo the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUND_Y = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'sprites/bird.png' 
BACKGROUND = 'sprites/background.png'
PIPE = 'sprites/pipe.png'

def welcome_Screen():
    """
    welcome Screen image on the Screen
    """
    player_x = int(SCREENWIDTH / 5)
    player_y = int(SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2
    message_x = int(SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2
    message_y = int(SCREENHEIGHT * 0.001)
    base_x = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['message'], (message_x, message_y))
                pygame.display.update()
                FPS_CLOCK.tick(FPS)


def main_Game():
    score = 0
    player_x = int(SCREENWIDTH / 5)
    player_y = int(SCREENWIDTH / 2)
    base_x = 0

    # Create 2 pipes for blitting on screen
    new_pipe_1 = getRandomPipe()
    new_pipe_2 = getRandomPipe()

    # List of upper pipe
    upper_pipes = [
        {'x': SCREENWIDTH + 200, 'y': new_pipe_1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': new_pipe_2[0]['y']},
    ]
    # List of lower pipe
    lower_pipes = [
        {'x': SCREENWIDTH + 200, 'y': new_pipe_1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': new_pipe_2[1]['y']},
    ]

    pipe_Vel_x = -4
    player_Vel_y = -9
    player_max_Vel_y = 10
    player_min_Vel_y = -8
    player_Acc_y = 1

    player_flap_acc = -8
    player_Flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    player_Vel_y = player_flap_acc
                    player_Flapped = True
                    GAME_SOUNDS['wing'].play()
        chashTest = isCollide(player_x, player_y, upper_pipes, lower_pipes)
        # player is crashed
        if chashTest:
            return

        # check for score
        player_mid_pos = player_x + GAME_SPRITES['player'].get_width() / 2
        for pipe in upper_pipes:
            pipe_mid_pos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()
            if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4:
                score += 1
                print(f"Your score is {score }")
                GAME_SOUNDS['point'].play()

        if player_Vel_y < player_max_Vel_y and not player_Flapped:
            player_Vel_y += player_Acc_y

        if player_Flapped:
            player_Flapped = False
        player_height = GAME_SPRITES['player'].get_height()
        player_y = player_y + min(player_Vel_y, GROUND_Y - player_y - player_height)

        # move pipe to the left
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            upper_pipe['x'] += pipe_Vel_x
            lower_pipe['x'] += pipe_Vel_x

        # add a new pipe
        if 0<upper_pipes[0]['x']<5:
            new_pipe = getRandomPipe()
            upper_pipes.append(new_pipe[0])
            lower_pipes.append(new_pipe[1])

        # if the pipe is out of the screen, remove it
        if upper_pipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)

        # lets blit our sprite now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upper_pipe['x'], upper_pipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lower_pipe['x'], lower_pipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (base_x, GROUND_Y))
        SCREEN.blit(GAME_SPRITES['player'], (player_x, player_y))
        my_digit = [int(x) for x in list(str(score))]
        width = 0
        for digit in my_digit:
            width += GAME_SPRITES['numbers'][digit].get_width()
        X_offset = (SCREENWIDTH - width) / 2

        for digit in my_digit:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (X_offset, SCREENHEIGHT * 0.12))
            X_offset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def isCollide(player_x, player_y, upper_pipes, lower_pipes):
    if player_y> GROUND_Y - 25  or player_y<0: 
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upper_pipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(player_y < pipeHeight + pipe['y'] and abs(player_x - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lower_pipes:
        if (player_y + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(player_x - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False
 

    return False


def getRandomPipe():
    """
    Generate position of two pipes ( one bottom straight and one top rotated ) for blitting on the Screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randint(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipe_x = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipe_x, 'y': -y1},
        {'x': pipe_x, 'y': y2}
    ]
    return pipe


if __name__ == '__main__':
    # This will be the main point from where our game will start
    pygame.init()  # Initialize all pygame's modules
    FPS_CLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('sprites/0.png').convert_alpha(),
        pygame.image.load('sprites/1.png').convert_alpha(),
        pygame.image.load('sprites/2.png').convert_alpha(),
        pygame.image.load('sprites/3.png').convert_alpha(),
        pygame.image.load('sprites/4.png').convert_alpha(),
        pygame.image.load('sprites/5.png').convert_alpha(),
        pygame.image.load('sprites/6.png').convert_alpha(),
        pygame.image.load('sprites/7.png').convert_alpha(),
        pygame.image.load('sprites/8.png').convert_alpha(),
        pygame.image.load('sprites/9.png').convert_alpha(),
    )        
    GAME_SPRITES['message'] = pygame.image.load('sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
                            pygame.image.load(PIPE).convert_alpha())

    # Game Sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcome_Screen()  # Shows welcome screen to the user until he presses a button
        main_Game()  # This is the main game function
 