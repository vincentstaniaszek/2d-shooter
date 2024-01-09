import pygame
from Game import *
import sys

# colours
GREEN = (0, 255, 0)
FPS = 60

# Constants
# GRAVITY = 1

pygame.init()
surface = pygame.display.set_mode([1600, 900])
pygame.display.set_caption("2D shooter")
moveRight = False
moveLeft = False


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, Mhealth, speed):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.scale = scale
        self.speed = speed
        self.Mhealth = Mhealth
        self.health = Mhealth
        self.img = pygame.image.load("_Idle.png")
        self.image = pygame.transform.scale_by(self.img, scale)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.oGravity = -0.5
        self.Gravity = -0.4
        self.vel = 0

    def updateX(self, L, R):
        if L:
            self.x = self.x + -10 * self.speed
            rect = self.img.get_rect()
            rect.center = (self.x, self.y)
            self.rect.center = (self.x, self.y)

        if R:
            self.x = self.x + 10 * self.speed
            rect = self.img.get_rect()
            rect.center = (self.x, self.y)
            self.rect.center = (self.x, self.y)

    def updateY(self, n):
        self.y = self.y + n
        rect = self.img.get_rect()
        rect.center = (self.x, self.y)
        self.rect.center = (self.x, self.y)

    def getHealth(self):
        return self.health

    def updateHealth(self, damage):
        self.health = self.health - damage
        print(self.health)
        if self.health <= 0:
            self.death()
        else:
            pass

    def velocity(self):
        self.vel = self.vel - self.Gravity
        self.updateY(self.vel)


    # def jump(self):


    def death(self):
        dead = True
        print("dead")

    def collisionCheck(self):
        print(self.rect.center)
        if 594 < self.rect.center[1] < 680 and self.vel >= 0:
            self.Gravity = 0
            self.vel = 0
            return True
        else:
            self.Gravity = self.oGravity
            return False


def draw(x1, y1, x2, y2, width):
    pygame.draw.rect(surface, GREEN, (x1, y1, x2, y2), width)

player = Character(200, 200, 5, 100, 1)

Jump = False

clock = pygame.time.Clock()
while True:

    surface.fill((43, 163, 212))

    floor = draw(100, 700, 1000, 100, 10)
    player.updateX(moveLeft, moveRight)


    if Jump and player.collisionCheck():
        player.vel = -15
        Jump = False

    player.velocity()
    player.collisionCheck()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # if event.type == pygame.joystick:
        #     if event.type == pygame.

        if event.type == pygame.KEYDOWN:
            # pygame.key.set_repeat(10, 2)
            if event.key == pygame.K_a:
                moveLeft = True
            if event.key == pygame.K_d:
                moveRight = True
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                Jump = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moveLeft = False
            if event.key == pygame.K_d:
                moveRight = False
            if event.key == pygame.K_SPACE:
                Jump = False


    surface.blit(player.image, player.rect)

    # pygame.display.update()
    pygame.display.flip()
    clock.tick(60)
    clock.tick()
    # print(clock.get_fps())

pygame.quit()
