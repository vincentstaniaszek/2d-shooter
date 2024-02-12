import random
import pygame
import sys
import os

pygame.init()
pygame.mixer.init()
pygame.display.init()
pygame.font.init()
pygame.Surface((1600, 900))
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("2D shooter")
from time import time

WAITING_INTERVAL = 20000000
start = time()
# pygame.display.set_mode((1600, 900))

# Colours
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SILVER = (175, 179, 176)

# Constants
FPS = 60

# Audio
shoot = pygame.mixer.Sound(os.path.join("audio", "Gun sounds", "9mm-pistol-shot.mp3"))
pygame.mixer.Sound.set_volume(shoot, 0.3)
walking = pygame.mixer.Sound(os.path.join("audio", "concrete-footsteps.mp3"))
pygame.mixer.Sound.set_volume(walking, 0.3)

# Backgrounds
Background1 = pygame.image.load(os.path.join("Backgrounds", "Background 1", "War.png")).convert_alpha()
ground = pygame.image.load(os.path.join("Backgrounds", "Background 1", "road.png")).convert_alpha()

# Animations
# Player
player_idle_right = pygame.image.load(os.path.join("Sprites", "Soldier 1", "idle(2).png")).convert_alpha()
player_shoot_right = pygame.image.load(os.path.join("Sprites", "Soldier 1", "shot_2(1).png")).convert_alpha()
player_running_right = pygame.image.load(os.path.join("Sprites", "Soldier 1", "Run2.png")).convert_alpha()
player_idle_left = pygame.image.load(os.path.join("Sprites", "Soldier 1", "idle(2)_left.png")).convert_alpha()
player_shoot_left = pygame.image.load(os.path.join("Sprites", "Soldier 1", "shot_2(1)_left.png")).convert_alpha()
player_running_left = pygame.image.load(os.path.join("Sprites", "Soldier 1", "Run2_left.png")).convert_alpha()
player_death_right = pygame.image.load(os.path.join("Sprites", "Soldier 1", "Dead_right.png")).convert_alpha()
player_death_left = pygame.image.load(os.path.join("Sprites", "Soldier 1", "Dead_left.png")).convert_alpha()
# Enemy
enemy_idle_right = pygame.image.load(os.path.join("Sprites", "Soldier 2", "idle2.png")).convert_alpha()
enemy_idle_left = pygame.image.load(os.path.join("Sprites", "Soldier 1", "idle(2)_left.png")).convert_alpha()
enemy_shoot_right = pygame.image.load(os.path.join("Sprites", "Soldier 2", "shot_1(2).png")).convert_alpha()
enemy_shoot_left = pygame.image.load(os.path.join("Sprites", "Soldier 1", "shot_2(1)_left.png")).convert_alpha()
enemy_walk_right = pygame.image.load(os.path.join("Sprites", "Soldier 2", "Walk2.png")).convert_alpha()
enemy_walk_left = pygame.image.load(os.path.join("Sprites", "Soldier 1", "Run2_left.png")).convert_alpha()
# enemy_death_right = pygame.image.load(os.path.join("Sprites", "Soldier 2", "Dead_right.png")).convert_alpha()
# enemy_death_left = pygame.image.load(os.path.join("Sprites", "Soldier 1", "Dead_left.png")).convert_alpha()

update = 100
cooldown = 750

# Text
health = pygame.font.SysFont("Comic Sans MS", 30)
ammo = pygame.font.SysFont("Comic Sans MS", 30)


def get_image(sheet, frame, width, height, scale, colour):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colour)
    return image


current_time = pygame.time.get_ticks()


# last_up = current_time


class wait():
    def __init__(self):
        self.current_time = pygame.time.get_ticks()
        self.last_up = 1000

    def wait1(self, time):
        print("c!", self.current_time)
        print("LU", self.last_up)
        print("T", time)
        if self.current_time - self.last_up >= time:
            print("yay")
            self.last_up = self.current_time
            return True


animation_list = []


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
        self.img = pygame.image.load(os.path.join("Sprites", "Soldier 1", "Idle.png")).convert_alpha()
        self.img = pygame.image.load("_idle.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.img, scale)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.oGravity = -0.6
        self.Gravity = -0.4
        self.vel = 0
        self.direction = "RIGHT"
        self.maxBullets = 5
        self.state = "idle"
        self.animation_cooldown = 100
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.bullets = []
        self.ammunition = pygame.image.load("RBullet.png").convert_alpha()
        self.ammunition = pygame.transform.scale_by(self.ammunition, 3)
        self.ammoVisual = []

        if len(self.ammoVisual) < 5:
            for i in range(5 - len(self.bullets)):
                self.ammoVisual.append((1040, -150 - 10 * (len(self.ammoVisual))))

    def updateX(self, L, R):
        """
        :param L: True if facing Left
        :param R: True if facing Right
        :return:
        """
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

    def getHealth(self) -> int:
        return self.health

    def updateHealth(self, damage):
        self.health = self.health - damage
        if self.health <= 0:
            self.death()
        else:
            pass

    def inputs(self):
        pass

    def velocity(self):
        self.vel = self.vel - self.Gravity
        self.updateY(self.vel)

    def death(self):
        print("dead")
        return True

    def collisionCheck(self):

        # print(self.rect.center)
        if 594 < self.rect.center[1] < 680 and self.vel >= 0:
            self.Gravity = 0
            self.vel = 0
            return True
        else:
            self.Gravity = self.oGravity
            return False

    def bulletManage(self):

        for bullet in self.bullets:
            bullet.draw()

            if bullet.hitCheck(self.rect):
                print("hit")
                self.bullets.pop(self.bullets.index(bullet))
            if 1600 > bullet.x > 0:
                bullet.x += bullet.speed
            else:
                self.ammoVisual.append((1040, -150 - 10 * (len(self.ammoVisual))))
                if len(self.ammoVisual) > 0:
                    self.bullets.pop(self.bullets.index(bullet))

        for i in self.ammoVisual:
            # print(len(self.ammoVisual))
            screen.blit(self.ammunition, i)
            # screen.blit(i, (1040, -200 + 10 * (len(self.ammoVisual))))
            # pygame.draw.circle(screen, RED, (1040, 0 + 10 * (len(self.ammoVisual))), 7)

        # self.rect = get_image(player_running, i, 128, 67, 3, WHITE)


class Player(Character):
    def __init__(self, x, y, scale):
        super().__init__(x, y, scale, 100, 1)

    def UI(self):
        # Health Bar
        pygame.draw.rect(screen, SILVER, (10, 40, 400, 40), 20)
        pygame.draw.rect(screen, BLACK, (5, 35, 410, 50), 5)
        self.bar = pygame.Rect(10, 40, 4 * self.health, 40)
        pygame.draw.rect(screen, RED, self.bar, 50)
        healthcount = health.render(("Health:" + str(player1.health)), True, (0, 0, 0))
        screen.blit(healthcount, (10, 35))
        # Ammunition count
        pygame.draw.rect(screen, (70, 70, 70), (1350, 0, 400, 100))
        pygame.draw.rect(screen, BLACK, (1360, 15, 45, 80))
        ammunition = ammo.render(("Ammo:" + str(5 - len(self.bullets)) + "/" + str(self.maxBullets)), True,
                                 (0, 0, 0))
        screen.blit(ammunition, (1420, 35))

    def shoot(self):
        if len(self.ammoVisual) > 0:
            self.ammoVisual.pop()
        self.state = "firing"
        if len(self.bullets) < self.maxBullets:
            pygame.mixer.Sound.play(shoot)
            self.bullets.append(
                Projectile((self.rect.center[0], self.rect.center[1] - 30), 20, self.direction, RED))

    def animationManage(self):
        self.c_time = pygame.time.get_ticks()
        if self.state == "idle":
            animation_steps = 4
            animation_list = []
            if self.direction == "RIGHT":
                for i in range(animation_steps):
                    animation_list.append(get_image(player_idle_right, i, 128, 67, 3, WHITE))
                if self.c_time - self.last_update >= self.animation_cooldown:
                    self.frame += 1
                    if self.frame >= len(animation_list):
                        self.frame = 0
                    self.last_update = self.c_time
            if self.direction == "LEFT":
                for i in range(animation_steps):
                    animation_list.append(get_image(player_idle_left, i, 128, 67, 3, WHITE))
                if self.c_time - self.last_update >= self.animation_cooldown:
                    self.frame += 1
                    if self.frame >= len(animation_list):
                        self.frame = 0
                    self.last_update = self.c_time

        if self.state == "firing":
            animation_steps = 4
            animation_list = []
            if self.direction == "RIGHT":
                for i in range(animation_steps):
                    animation_list.append(get_image(player_shoot_right, i, 128, 64, 3, WHITE))
                if self.c_time - self.last_update >= self.animation_cooldown:
                    self.frame += 1
                    if self.frame >= len(animation_list):
                        self.frame = 0
                    self.last_update = self.c_time
            if self.direction == "LEFT":
                for i in range(animation_steps):
                    animation_list.append(get_image(player_shoot_left, i, 128, 64, 3, WHITE))
                if self.c_time - self.last_update >= self.animation_cooldown:
                    self.frame += 1
                    if self.frame >= len(animation_list):
                        self.frame = 0
                    self.last_update = self.c_time

        if self.state == "running":
            animation_steps = 4
            animation_list = []
            if self.direction == "RIGHT":
                for i in range(animation_steps):
                    animation_list.append(get_image(player_running_right, i, 128, 61, 3, WHITE))
                if self.c_time - self.last_update >= self.animation_cooldown:
                    self.frame += 1
                    if self.frame >= len(animation_list):
                        self.frame = 0
                    self.last_update = self.c_time
            if self.direction == "LEFT":
                for i in range(animation_steps):
                    animation_list.append(get_image(player_running_left, i, 128, 61, 3, WHITE))
                if self.c_time - self.last_update >= self.animation_cooldown:
                    self.frame += 1
                    if self.frame >= len(animation_list):
                        self.frame = 0
                    self.last_update = self.c_time

        # if self.getHealth() <= 0:
        #     animation_steps = 4
        #     animation_list = []
        #     if self.direction == "RIGHT":
        #         for i in range(animation_steps):
        #             animation_list.append(get_image(player_death_right, i, 128, 62, 3, WHITE))
        #         if self.c_time - self.last_update >= self.animation_cooldown:
        #             self.frame += 1
        #             if self.frame >= len(animation_list):
        #                 self.played = True
        #                 self.frame = 0
        #             self.last_update = self.c_time
        #
        #     if self.direction == "LEFT":
        #         for i in range(animation_steps):
        #             animation_list.append(get_image(player_death_left, i, 128, 62, 3, WHITE))
        #         if self.c_time - self.last_update >= self.animation_cooldown:
        #             self.frame += 1
        #             if self.frame >= len(animation_list):
        #                 self.played = True
        #                 self.frame = 0
        #             self.last_update = self.c_time
        if self.state == "null":
            pass

        screen.blit((animation_list[self.frame]), (self.x - 180, self.y - 100))


class Enemy(Character):
    def __init__(self, x, y, scale):
        super().__init__(x, y, scale, 100, 0.3)
        self.t = pygame.time.get_ticks()
        self.T = self.t + 500
        self.maxBullets = 1
        self.move = random.randint(-1, 1)

    def healthBar(self):
        pygame.draw.rect(screen, SILVER, (self.x - 45, self.y - 120, 100, 5), 20)
        pygame.draw.rect(screen, BLACK, (self.x - 50, self.y - 125, 110, 15), 5)
        self.bar = pygame.Rect(self.x - 45, self.y - 120, 1 * self.health, 5)
        pygame.draw.rect(screen, RED, self.bar, 50)

    def shoot(self):
        self.state = "firing"
        if time() - start >= WAITING_INTERVAL:
            print("yaya")
        if len(self.bullets) < self.maxBullets:
            pygame.mixer.Sound.play(shoot)
            self.bullets.append(
                Projectile((self.rect.center[0], self.rect.center[1] - 30), 20, self.direction, RED))

    def vision(self, target_x, target_y):
        x = self.x
        if self.direction == "RIGHT":
            for i in range(600):
                if target_x - 50 < self.x + i < target_x + 50:
                    # print("great success")
                    return True
        if self.direction == "LEFT":
            for i in range(600):
                if target_x - 50 < self.x - i < target_x + 50:
                    # print("great success")
                    return True
            # else:
            #     return False
        self.x = x

    def movement(self):
        self.c_time = pygame.time.get_ticks()
        if self.move == 1:
            self.updateX(0, 1)
            self.state = "walking"
            self.direction = "RIGHT"
            print("c", self.c_time)
            print("u", self.last_update)
            # print("", )
            if self.c_time - self.last_update + random.randint(50, 200) >= 200:
                self.move = 0
                self.last_update = self.c_time
        print(self.move)
        if self.move == -1:
            self.updateX(1, 0)
            self.state = "walking"
            self.direction = "LEFT"
            print("c", self.c_time)
            print("u", self.last_update)
            # print("", )
            if self.c_time - self.last_update >= 100:
                self.move = 0
                self.last_update = self.c_time
        if self.move == 0:
            self.state = "idle"
            if self.c_time - self.last_update >= 100:
                self.move = random.randint(-1, 1)
                self.last_update = self.c_time

    def AI(self):
        self.movement()
        if self.vision(player1.x, player1.y):
            enemy.shoot()

    def animationManage(self):
        self.c_time = pygame.time.get_ticks()
        if self.state == "idle":
            animation_steps = 4
            animation_list = []
            if self.direction == "RIGHT":
                for i in range(animation_steps):
                    animation_list.append(get_image(enemy_idle_right, i, 128, 63, 3, WHITE))
                if self.c_time - self.last_update >= self.animation_cooldown:
                    self.frame += 1
                    if self.frame >= len(animation_list):
                        self.frame = 0
                    self.last_update = self.c_time
            if self.direction == "LEFT":
                for i in range(animation_steps):
                    animation_list.append(get_image(enemy_idle_left, i, 128, 63, 3, WHITE))
                if self.c_time - self.last_update >= self.animation_cooldown:
                    self.frame += 1
                    if self.frame >= len(animation_list):
                        self.frame = 0
                    self.last_update = self.c_time

        if self.state == "firing":
            animation_steps = 4
            animation_list = []
            if self.direction == "RIGHT":
                for i in range(animation_steps):
                    animation_list.append(get_image(enemy_shoot_right, i, 128, 62, 3, WHITE))
                if self.c_time - self.last_update >= self.animation_cooldown:
                    self.frame += 1
                    if self.frame >= len(animation_list):
                        self.frame = 0
                    self.last_update = self.c_time
            if self.direction == "LEFT":
                for i in range(animation_steps):
                    animation_list.append(get_image(enemy_shoot_left, i, 128, 62, 3, WHITE))
                if self.c_time - self.last_update >= self.animation_cooldown:
                    self.frame += 1
                    if self.frame >= len(animation_list):
                        self.frame = 0
                    self.last_update = self.c_time

        if self.state == "walking":
            animation_steps = 4
            animation_list = []
            if self.direction == "RIGHT":
                for i in range(animation_steps):
                    animation_list.append(get_image(enemy_walk_right, i, 128, 65, 3, WHITE))
                if self.c_time - self.last_update >= self.animation_cooldown:
                    self.frame += 1
                    if self.frame >= len(animation_list):
                        self.frame = 0
                    self.last_update = self.c_time
            if self.direction == "LEFT":
                for i in range(animation_steps):
                    animation_list.append(get_image(enemy_walk_left, i, 128, 61, 3, WHITE))
                if self.c_time - self.last_update >= self.animation_cooldown:
                    self.frame += 1
                    if self.frame >= len(animation_list):
                        self.frame = 0
                    self.last_update = self.c_time

        if self.state == "null":
            pass

        screen.blit((animation_list[self.frame]), (self.x - 180, self.y - 100))


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


delay = wait()
player1 = Player(200, 200, 5)

Jump = False

# bullets = []
enemies = []
update1 = pygame.time.get_ticks() + 200
clock = pygame.time.Clock()
while True:
    player1.updateX(moveLeft, moveRight)
    # current_time = pygame.time.get_ticks()
    # if current_time - last_update >= animation_cooldown:
    #     if frame > 5:
    #         frame = 0
    #     else:
    #         frame += 1
    #         last_update = current_time

    tick = pygame.time.get_ticks()

    if player1.state == "firing":
        if tick - update > cooldown:
            player1.state = "idle"
            update = tick

    if Jump and player1.collisionCheck():
        player1.vel = -15
        Jump = False

    player1.velocity()
    player1.collisionCheck()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moveLeft = True
                pygame.mixer.Sound.play(walking)
                player1.direction = "LEFT"
                player1.state = "running"
            if event.key == pygame.K_d:
                pygame.mixer.Sound.play(walking)
                moveRight = True
                player1.state = "running"
                player1.direction = "RIGHT"
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                Jump = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_j:
                player1.shoot()
            if event.key == pygame.K_l:
                # enemies.append(Enemy(random.randint(30, 1570), 300, 5))
                enemies.append(Enemy(1000, 300, 5))
            if event.key == pygame.K_p:
                player1.health = player1.health - 32
                # delay.wait1(100)
                # if time() - start >= WAITING_INTERVAL:
                #     print("yayay")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moveLeft = False
                player1.state = "idle"
                pygame.mixer.Sound.stop(walking)
            if event.key == pygame.K_d:
                moveRight = False
                player1.state = "idle"
                pygame.mixer.Sound.stop(walking)
            if event.key == pygame.K_SPACE:
                Jump = False
    loadBack(1)

    # screen.blit(player.image, player.rect)
    # pygame.draw.rect(screen, RED, player.rect)

    player1.animationManage()
    for enemy in enemies:
        enemy.velocity()
        enemy.collisionCheck()
        enemy.animationManage()
        enemy.healthBar()
        enemy.AI()
        enemy.bulletManage()
        for bullet in enemy.bullets:
            if bullet.hitCheck(player1.rect):
                player1.updateHealth(1)
                print("hit")
                enemy.bullets.pop(enemy.bullets.index(bullet))
        for bullet in player1.bullets:
            if bullet.hitCheck(enemy.rect):
                enemy.updateHealth(25)
                print("hit")
                player1.ammoVisual.append((1040, -150 - 10 * (len(player1.ammoVisual))))
                player1.bullets.pop(player1.bullets.index(bullet))

        if enemy.getHealth() <= 0:
            if enemy.c_time - update1 >= 2000:
                enemies.pop(enemies.index(enemy))

    # pygame.time.set_timer()
    # player1.healthBar()
    # player1.ammoCounter()
    # print(player1.x)
    # print(player1.rect)
    player1.UI()
    player1.bulletManage()
    pygame.display.flip()
    clock.tick(60)
    # print(clock.get_fps())

# pygame.quit()
