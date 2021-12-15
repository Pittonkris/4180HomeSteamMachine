import pygame, sys
from pygame.constants import JOYAXISMOTION
from pygame.locals import *
import random, time


pygame.init()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
#print(joysticks)
#joysticks[0].init()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 60

FramePerSec = pygame.time.Clock()

y_pos = 0
speed = 5
lives = 1
bodies = 1
time = 0
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = "opening screen"

font_big_clear = pygame.font.Font("fonts/white_font.ttf", 60)
font_small_clear = pygame.font.Font("fonts/white_font.ttf", 20)
font_big_bold = pygame.font.Font("fonts/black_font.ttf", 60)
font_small_bold = pygame.font.Font("fonts/black_font.ttf", 20)

lives = font_small_clear.render("LIVES: " + str(lives), True, WHITE)
time = font_small_clear.render("TIME: " + str(time), True, WHITE)

opening = pygame.image.load("pics/opening.png")
game_over = pygame.image.load("pics/game_over.png")
lives_page = pygame.image.load("pics/lives.png")
bodies_page = pygame.image.load("pics/bodies.png")

DISPLAYSURF = pygame.display.set_mode((600,400), pygame.FULLSCREEN)
DISPLAYSURF.fill(BLACK)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pics/dog.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    def move(self):
        global y_pos
        self.rect.bottom = y_pos
        if self.rect.bottom > 1.2*SCREEN_HEIGHT:
            y_pos = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -22)
        print("self.rect.x:" + str(self.rect.x))
        print("self.rect.y:" + str(self.rect.y))
        print("self.rect.top: " + str(self.rect.top))
        print("self.rect.bottom: " + str(self.rect.bottom))
        print("self.rect.center: " + str(self.rect.center))
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pics/buzz.png")
        self.rect = self.image.get_rect()
        print(self.rect)
        self.rect.center = (350, 300)
        self.stick = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self):
        if self.stick == 0:
            axis = 2
        else:
            axis = 0
        self.rect.move_ip(10*joysticks[0].get_axis(axis), 10*joysticks[0].get_axis(axis + 1))
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

player1 = Player()
player2 = Player()
player2.rect.x = 300
player2.stick = 1
enemy = Enemy()

enemies = pygame.sprite.Group()
enemies.add(enemy)
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)
all_sprites.add(enemy)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 500)

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if screen == "opening screen":
            DISPLAYSURF.blit(opening, (0, 0))
            if event.type == JOYBUTTONDOWN:
                if event.button == 0:
                    screen = "1 player bodies option"
                    break
                if event.button == 1:
                    screen = "2 player"
                    break
                if event.button == 2:
                    pygame.quit()
                    sys.exit()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        elif screen == "1 player bodies option":
            DISPLAYSURF.blit(bodies_page, (0,0))
            if event.type == JOYBUTTONDOWN:
                if event.button == 0:
                    screen = "lives option"
                    break
                if event.button == 1:
                    screen = "1 player 2 bodies"
                    bodies = 2
                    break
                if event.button == 2:
                    screen = "opening screen"
                    break
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        elif screen == "lives option":
            DISPLAYSURF.blit(lives_page, (0,0))
            if event.type == JOYBUTTONDOWN:
                if event.button == 0:
                    screen = "1 player 1 body"
                    lives = 1
                    break
                if event.button == 1:
                    screen = "1 player 1 body"
                    lives = 2
                    break
                if event.button == 2:
                    screen = "1 player bodies option"
                    break
                if event.button == 3:
                    screen = "1 player 1 body"
                    lives = 3
                    break
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        elif screen == "1 player 1 body":
            DISPLAYSURF.fill(BLACK)
            DISPLAYSURF.blit(enemy.image, enemy.rect)
            DISPLAYSURF.blit(player1.image, player1.rect)
            if event.type == INC_SPEED:
                speed += 2
                y_pos += speed
                break
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            player1.move()
            enemy.move()
            if pygame.sprite.spritecollideany(player1, enemies):
                lives-=1
                if lives == 0:
                    screen = "game over"
                    break
                pygame.display.update()

        elif screen == "1 player 2 bodies":
            DISPLAYSURF.fill(BLACK)
            DISPLAYSURF.blit(enemy.image, enemy.rect)
            DISPLAYSURF.blit(player1.image, player1.rect)
            DISPLAYSURF.blit(player2.image, player2.rect)
            count_alive = 2
            if event.type == INC_SPEED:
                if speed <= 50:
                    speed += 2
                y_pos += speed
                break
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            player1.move()
            player2.move()
            enemy.move()
            if pygame.sprite.spritecollideany(player1, enemies):
                player1.kill()
                count_alive-=1
                if count_alive == 0:
                    screen = "game over"
                    break
            if pygame.sprite.spritecollideany(player2, enemies):
                player2.kill()
                count_alive-=1
                if count_alive == 0:
                    screen = "game over"
                    break

        elif screen == "2 player":
            DISPLAYSURF.fill(BLACK)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        elif screen == "game over":
            DISPLAYSURF.blit(game_over, (0, 0))
            if event.type == JOYBUTTONDOWN:
                if event.button == 0:
                    screen = "opening screen"
                    break
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    player1.move()
    enemy.move()

    # Moves and Re-draws all Sprites
    #for entity in all_sprites:
        #DISPLAYSURF.blit(entity.image, entity.rect)
        #entity.move()

    #To be run if collisio

    pygame.display.update()
    FramePerSec.tick(FPS)
