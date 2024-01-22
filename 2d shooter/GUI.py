import pygame
from Game import *
import sys
import os
pygame.mixer.init()

# colours
GREEN = (0, 255, 0)
FPS = 60
RED = (235, 64, 52)
# Constants
# GRAVITY = 1

shoot = pygame.mixer.Sound(os.path.join("audio", "Gun sounds", "9mm-pistol-shot.mp3"))
walking = pygame.mixer.Sound(os.path.join("audio", "concrete-footsteps.mp3"))

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
        # self.img = pygame.image.load(os.path.join("Sprites","Soldier 1", "Idle.png"))
        self.img = pygame.image.load("_idle.png")
        self.image = pygame.transform.scale_by(self.img, scale)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.oGravity = -0.5
        self.Gravity = -0.4
        self.vel = 0
        self.direction = "RIGHT"
        self.maxBullets = 3

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
        # print(self.rect.center)
        if 594 < self.rect.center[1] < 680 and self.vel >= 0:
            self.Gravity = 0
            self.vel = 0
            return True
        else:
            self.Gravity = self.oGravity
            return False


class projectile(pygame.sprite.Sprite):
    def __init__(self, center, speed, direction, colour):
        pygame.sprite.Sprite.__init__(self)
        self.center = center
        self.x = center[0] + 60
        self.y = center[1] - 30
        self.speed = speed
        self.colour = colour
        self.direction = direction
        if self.direction == "LEFT":
            self.speed = -self.speed
            self.x = center[0] - 60

    def hitCheck(self, targetCoords):
        # print(targetCoords[0])
        # print(self.x)
        if targetCoords[0] <= self.x <= (targetCoords[2] + targetCoords[0]) :
            return True
        else:
            return False

    def draw(self):
        pygame.draw.circle(surface, self.colour, (self.x, self.y), 7)


def draw(x1, y1, x2, y2, width):
    pygame.draw.rect(surface, GREEN, (x1, y1, x2, y2), width)

player = Character(200, 200, 5, 100, 1)

Jump = False

bullets = []

clock = pygame.time.Clock()
while True:
    surface.fill((43, 163, 212))
    floor = draw(100, 700, 1000, 100, 10)
    player.updateX(moveLeft, moveRight)

    if Jump and player.collisionCheck():
        player.vel = -15
        Jump = False

    for bullet in bullets:
        if bullet.x < 1600 and bullet.x > 0:
            bullet.x += bullet.speed
        else:
            bullets.pop(bullets.index(bullet))

    player.velocity()
    player.collisionCheck()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # pygame.key.set_repeat(10, 2)
            if event.key == pygame.K_a:
                moveLeft = True
                pygame.mixer.Sound.play(walking)
                player.direction = "LEFT"
            if event.key == pygame.K_d:
                pygame.mixer.Sound.play(walking)
                moveRight = True
                player.direction = "RIGHT"
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                Jump = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_j:
                gun = True
                pygame.mixer.Sound.play(shoot)
                if len(bullets) < 5:
                    # bullets.append(projectile(player.rect.center, 15, player.direction, RED))
                    bullets.append(projectile((800,600), 15, player.direction, RED))

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moveLeft = False
                pygame.mixer.Sound.stop(walking)
            if event.key == pygame.K_d:
                moveRight = False
                pygame.mixer.Sound.stop(walking)
            if event.key == pygame.K_SPACE:
                Jump = False

    for bullet in bullets:
        if bullet.hitCheck(player.rect):
            print("hit")
            bullets.pop(bullets.index(bullet))

    for bullet in bullets:
        bullet.draw()
    surface.blit(player.image, player.rect)
    pygame.display.flip()
    clock.tick(60)
    # clock.tick()

pygame.quit()
