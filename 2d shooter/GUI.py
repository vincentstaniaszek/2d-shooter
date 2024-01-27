import pygame
from Game import *
import sys
import os

pygame.init()
pygame.mixer.init()
pygame.display.init()
pygame.Surface((1600, 900))
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("2D shooter")
# pygame.display.set_mode((1600, 900))

# Colours
GREEN = (0, 255, 0)
FPS = 60
RED = (235, 64, 52)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Constants
# GRAVITY = 1

# Audio
shoot = pygame.mixer.Sound(os.path.join("audio", "Gun sounds", "9mm-pistol-shot.mp3"))
walking = pygame.mixer.Sound(os.path.join("audio", "concrete-footsteps.mp3"))

# Backgrounds
Background1 = pygame.image.load(os.path.join("Backgrounds", "Background 1", "War.png")).convert_alpha()
ground = pygame.image.load(os.path.join("Backgrounds", "Background 1", "road.png")).convert_alpha()

# Animations
player_running = pygame.image.load(os.path.join("Sprites", "Soldier 1", "idle(2).png")).convert_alpha()


def get_image(sheet, frame, width, height, scale, colour):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colour)

    return image

animation_list = []
animation_steps = 7

# for i in range(animation_steps):
#     get_image(player_running, i, 128, 67, 3, WHITE)


# frame_0 = get_image(player_running, 0, 128, 67, 3, WHITE)
# frame_1 = get_image(player_running, 0, 256, 67, 3, WHITE)
# frame_2 = get_image(player_running, 0, 384, 67, 3, WHITE)
# frame_3 = get_image(player_running, 0, 512, 67, 3, WHITE)
# frame_4 = get_image(player_running, 0, 640, 67, 3, WHITE)
# frame_5 = get_image(player_running, 0, 768, 67, 3, WHITE)
# frame_6 = get_image(player_running, 0, 896, 67, 3, WHITE)

def loadBack(level):
    if level == 1:
        screen.blit(Background1, (0, 0))
        screen.blit(ground, (0, -210))


moveRight = False
moveLeft = False


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, max_health, speed):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.scale = scale
        self.speed = speed
        self.max_health = max_health
        self.health = max_health
        # self.img = pygame.image.load(os.path.join("Sprites","Soldier 1", "Idle.png"))
        self.img = pygame.image.load("_idle.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.img, scale)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.oGravity = -0.5
        self.Gravity = -0.4
        self.vel = 0
        self.direction = "RIGHT"
        self.maxBullets = 3
        self.state = "idle"

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

    def animationManage(self):
        # if self.state == "idle":
        for i in range(animation_steps):
            animation_list.append((get_image(player_running, i, 128, 67, 3, WHITE), (0, 0)))





class Projectile(pygame.sprite.Sprite):
    def __init__(self, center, speed, direction, colour):
        pygame.sprite.Sprite.__init__(self)
        self.center = center
        self.x = center[0] + 60
        self.y = center[1] - 30
        self.speed = speed
        self.colour = colour
        self.direction = direction
        # self.img = pygame.image.load("R_bullet.png")
        # self.image = pygame.transform.scale_by(self.img, scale)
        # self.rect = self.image.get_rect()

        if self.direction == "LEFT":
            self.speed = -self.speed
            self.x = center[0] - 60

    def hitCheck(self, targetCoords):
        # print(targetCoords[0])
        # print(self.x)
        if targetCoords[0] <= self.x <= (targetCoords[2] + targetCoords[0]):
            return True
        else:
            return False

    def draw(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), 7)


def draw(x1, y1, x2, y2, width):
    pygame.draw.rect(screen, GREEN, (x1, y1, x2, y2), width)


player = Character(200, 200, 5, 100, 1)

Jump = False

bullets = []

clock = pygame.time.Clock()
while True:
    # surface.fill((10, 163, 212))
    # pygame.screen.blit(Background1,(0, 0))
    # surface.blit(Background1, (0, 0))

    # floor = draw(100, 700, 1000, 100, 10)
    player.updateX(moveLeft, moveRight)

    if Jump and player.collisionCheck():
        player.vel = -15
        Jump = False

    for bullet in bullets:
        if 1600 > bullet.x > 0:
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
                    bullets.append(Projectile(player.rect.center, 15, player.direction, RED))
                    # bullets.append(projectile((800,600), 15, player.direction, RED))

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

    loadBack(1)
    for bullet in bullets:
        bullet.draw()
    screen.blit(player.image, player.rect)
    # screen.blit(frame_0, (0, 0))
    player.animationManage()
    for i in range(animation_steps):
        screen.blit(animation_list[i], (0, 0))
    pygame.display.flip()
    clock.tick(60)
    # print(clock.get_fps())

# pygame.quit()
