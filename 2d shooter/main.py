# Loading libraries
import random
import pygame
import sys
import os
import noise

# Initialising libraries
pygame.init()
pygame.mixer.init()
pygame.display.init()
pygame.font.init()

# surface
Height = 900
Width = 1600
pygame.Surface((1600, 900))
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("2D shooter")

# Colours
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SILVER = (175, 179, 176)
DARK_GREEN = (27, 41, 27)
GREY = (46, 45, 45)

# Constants
FPS = 60

# Variables
difficulty = "easy"
GAME_STATE = "menu"

# Audio
sound = True
shoot = pygame.mixer.Sound(os.path.join("audio", "Gun sounds", "9mm-pistol-shot.mp3"))
walking = pygame.mixer.Sound(os.path.join("audio", "concrete-footsteps.mp3"))


def muted(state):
    """
    Function to change game volume from on to off and vice versa
    :param state: Boolean value which is False when muted
    :return:
    """
    if state:
        pygame.mixer.Sound.set_volume(shoot, 0.3)
        pygame.mixer.Sound.set_volume(walking, 0.3)
    elif not state:
        print("muted")
        pygame.mixer.Sound.set_volume(shoot, 0)
        pygame.mixer.Sound.set_volume(walking, 0)


muted(sound)

# Backgrounds
Background1 = pygame.image.load(os.path.join("Backgrounds", "Background 1", "War.png")).convert_alpha()
Background2 = pygame.image.load(os.path.join("Backgrounds", "New background", "Background.png")).convert_alpha()
Background2 = pygame.transform.scale_by(Background2, 3)
ground = pygame.image.load(os.path.join("Backgrounds", "Background 1", "road.png")).convert_alpha()
ground2 = pygame.image.load(os.path.join("Backgrounds", "Ground", "Tile_22_long2.png")).convert_alpha()
ground2 = pygame.transform.scale_by(ground2, 5).convert_alpha()

# 0 - player1.camera_offset_x + player1.x + Width, 0
# sideScroll = []
# screen.blit(Background2, (0 - player1.camera_offset_x, 0))
# if (player1.camera_offset_x + Width) % 100 == 0:
#     sideScroll.append(Background2)
#     # screen.blit(Background2, (0 - player1.camera_offset_x + Width, 0))
#     # screen.blit(Background2, (0 - player1.camera_offset_x + 2 * Width, 0))
#     # screen.blit(Background2, (0 - player1.camera_offset_x + 3 * Width, 0))
#     # screen.blit(Background2, (0 - player1.camera_offset_x + 4 * Width, 0))
# else:
#     pass
# print(len(sideScroll))
# for i in range(len(sideScroll)):
#     for image in sideScroll:
#         screen.blit(image, (0 - player1.camera_offset_x + player1.x + i * Width, 0))
# screen.blit(ground, (0 - player1.camera_offset_x, -210))

blocks = []
blockRect = []


class tiles:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ground2 = pygame.image.load(os.path.join("Backgrounds", "Ground", "Tile_22_long.png")).convert()
        self.ground2 = pygame.transform.scale_by(self.ground2, 3)
        self.rect = self.ground2.get_rect()
        self.box = self.rect
        # print(self.rect)
        self.rect.center = (self.x, self.y + 85)
        blockRect.append(self.rect)

    def hitBox(self):
        pygame.draw.rect(screen, RED, (self.rect))

    def update(self):
        blockRect.append(self.rect)
        # self.box = self.ground2.get_rect()

    def wallCol(self, target_x, target_y):
        if self.rect.collidepoint(target_x, target_y):
            print("collision")


# for i in range(100):
#     print((noise.pnoise1((i * 0.01)) * 1000))
# height = int((noise.pnoise1((i * 0.0001) * 80000) + 500))
def genBlock(x):
    prevHeight = 300
    seed = random.randint(1, 100)
    print(seed)
    # seed = 121
    for i in range(100):
        height = int((noise.pnoise1((i * 0.1), persistence=10, repeat=9999, base=seed) * 300) + 600)
        height = round(height, -2)

        if 750 < height:
            height = 750
        elif i > 1 and height < 400:
            height = blocks[i-1].y

        # print(height)
        blocks.append(tiles(i*93, height))

    # height = int(noise.pnoise1(0.1, repeat=99999)) + 750
    # for i in range(len(blocks)):
    #     print(blocks[i].x, blocks[i].y



# height = noise.pnoise1(200*10, 10)
# print(height)

# for i in range(100):
#     for l in blocks:
#         blockRect.append(l.rect)


def loadBack(level):
    """
    Loads and blits background corresponding to the current level
    :param level: Integer value which denotes the backgrounds to be loaded
    :return:
    """
    if level == 1:
        screen.blit(Background2, (0 - player1.camera_offset_x, 0))
        screen.blit(Background2, (0 - player1.camera_offset_x + Width, 0))
        screen.blit(Background2, (0 - player1.camera_offset_x + 2 * Width, 0))
        screen.blit(Background2, (0 - player1.camera_offset_x + 3 * Width, 0))
        screen.blit(Background2, (0 - player1.camera_offset_x + 4 * Width, 0))
        screen.blit(Background2, (0 - player1.camera_offset_x - Width, 0))
        screen.blit(Background2, (0 - player1.camera_offset_x - 2 * Width, 0))
        screen.blit(Background2, (0 - player1.camera_offset_x - 3 * Width, 0))
        screen.blit(Background2, (0 - player1.camera_offset_x - 4 * Width, 0))
        for i in range(len(blocks)):
            for square in blocks:
                # square.x = square.x - player1.camera_offset_x

                square.rect = (square.x - player1.camera_offset_x + 47, square.y, 93, 300)
                screen.blit(square.ground2, square.rect)
                # print(square.rect)
                # print(blockRect)
                square.update()
                # square.hitBox()


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
enemy_idle_left = pygame.image.load(os.path.join("Sprites", "Soldier 2", "idle2_left.png")).convert_alpha()
enemy_shoot_right = pygame.image.load(os.path.join("Sprites", "Soldier 2", "shot_1(2).png")).convert_alpha()
enemy_shoot_left = pygame.image.load(os.path.join("Sprites", "Soldier 2", "shot_1(2)_left.png")).convert_alpha()
enemy_walk_right = pygame.image.load(os.path.join("Sprites", "Soldier 2", "Walk2.png")).convert_alpha()
enemy_walk_left = pygame.image.load(os.path.join("Sprites", "Soldier 2", "Walk2_left.png")).convert_alpha()
# enemy_death_right = pygame.image.load(os.path.join("Sprites", "Soldier 2", "Dead_right.png")).convert_alpha()
# enemy_death_left = pygame.image.load(os.path.join("Sprites", "Soldier 1", "Dead_left.png")).convert_alpha()

# (100,600,100, 100)


# buttons
play_button = (550, 330, 500, 110)
options_button = (550, 480, 500, 110)
exit_button = (550, 630, 500, 110)
mute_button = (550, 330, 500, 110)
difficulty_button = (550, 480, 500, 110)

update = 100
cooldown = 750

# Text
health = pygame.font.SysFont("Times New Roman", 30)
ammo = pygame.font.SysFont("Times New Roman", 30)


def get_image(sheet, frame, width, height, scale, colour):
    """
    Returns an image which is part of a sprite sheet depending on the current frame
    :param sheet: Image(sprite sheet)
    :param frame: The current frame/step in the animation
    :param width: The width of each part of the sheet
    :param height: The height of the image in the sheet
    :param scale: The size of the image that it returned
    :param colour: Takes in a colour value in order to remove that colour from the image
    :return: Section of the sprite sheet
    """
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colour)
    return image


def mainMenu():
    """
    Draws all the boxes and text for the main menu
    :return:
    """
    screen.fill(DARK_GREEN)
    pygame.draw.rect(screen, GREY, play_button)
    pygame.draw.rect(screen, GREY, options_button)
    pygame.draw.rect(screen, GREY, exit_button)
    screen.blit(pygame.font.SysFont("Times New Roman", 30).render("LEVEL SELECT", True, WHITE, ), (700, 365))
    screen.blit(pygame.font.SysFont("Times New Roman", 30).render("OPTIONS", True, WHITE, ), (730, 515))
    screen.blit(pygame.font.SysFont("Times New Roman", 30).render("EXIT", True, WHITE, ), (765, 665))


def menuControls():
    """
    Uses the variable game_state in order to allow buttons to be pressed using a mouse
    :return:
    """
    global GAME_STATE
    global sound
    global difficulty
    if GAME_STATE == "menu":
        if event.type == pygame.MOUSEBUTTONDOWN and play_button[0] < pygame.mouse.get_pos()[0] < play_button[
            0] + 500 and \
                play_button[1] < pygame.mouse.get_pos()[1] < play_button[1] + 110:
            GAME_STATE = "playing"
        if event.type == pygame.MOUSEBUTTONDOWN and options_button[0] < pygame.mouse.get_pos()[0] < options_button[0] \
                + 500 and options_button[1] < pygame.mouse.get_pos()[1] < options_button[1] + 110:
            GAME_STATE = "options"
        if event.type == pygame.MOUSEBUTTONDOWN and exit_button[0] < pygame.mouse.get_pos()[0] < exit_button[
            0] + 500 and \
                exit_button[1] < pygame.mouse.get_pos()[1] < exit_button[1] + 110:
            pygame.quit()
    elif GAME_STATE == "options":
        if sound and event.type == pygame.MOUSEBUTTONDOWN and mute_button[0] < pygame.mouse.get_pos()[0] < mute_button[
            0] + 500 and \
                mute_button[1] < pygame.mouse.get_pos()[1] < mute_button[1] + 110:
            sound = False
            muted(sound)
        elif not sound and event.type == pygame.MOUSEBUTTONDOWN and mute_button[0] < pygame.mouse.get_pos()[0] < \
                mute_button[
                    0] + 500 and \
                mute_button[1] < pygame.mouse.get_pos()[1] < mute_button[1] + 110:
            sound = True
            muted(sound)
        if difficulty == "easy" and event.type == pygame.MOUSEBUTTONDOWN and difficulty_button[0] < \
                pygame.mouse.get_pos()[0] < difficulty_button[0] + 500 \
                and difficulty_button[1] < pygame.mouse.get_pos()[1] < difficulty_button[1] + 110:
            difficulty = "hard"
        elif difficulty == "hard" and event.type == pygame.MOUSEBUTTONDOWN and difficulty_button[0] < \
                pygame.mouse.get_pos()[0] < difficulty_button[0] \
                + 500 and difficulty_button[1] < pygame.mouse.get_pos()[1] < difficulty_button[1] + 110:
            difficulty = "easy"
        if event.type == pygame.MOUSEBUTTONDOWN and exit_button[0] < pygame.mouse.get_pos()[0] < exit_button[0] \
                + 500 and exit_button[1] < pygame.mouse.get_pos()[1] < exit_button[1] + 110:
            GAME_STATE = "menu"

    elif GAME_STATE == "death":
        if event.type == pygame.MOUSEBUTTONDOWN and options_button[0] < pygame.mouse.get_pos()[0] < \
                options_button[0] + 500 and options_button[1] < pygame.mouse.get_pos()[1] < options_button[1] + 110:
            GAME_STATE = "menu"

        if event.type == pygame.MOUSEBUTTONDOWN and exit_button[0] < pygame.mouse.get_pos()[0] < exit_button[
            0] + 500 and \
                exit_button[1] < pygame.mouse.get_pos()[1] < exit_button[1] + 110:
            pygame.quit()


# Defines the players default traveling direction
moveRight = False
moveLeft = False


def options():
    """
    Draws all the boxes and text for the options screen
    :return:
    """
    global GAME_STATE
    screen.fill(DARK_GREEN)
    pygame.draw.rect(screen, GREY, mute_button)
    pygame.draw.rect(screen, GREY, difficulty_button)
    pygame.draw.rect(screen, GREY, exit_button)
    if sound:
        screen.blit(pygame.font.SysFont("Times New Roman", 30).render("MUTE", True, WHITE, ), (760, 365))
    elif not sound:
        screen.blit(pygame.font.SysFont("Times New Roman", 30).render("UNMUTE", True, WHITE, ), (740, 365))
    if difficulty == "easy":
        screen.blit(pygame.font.SysFont("Times New Roman", 30).render("DIFFICULTY EASY", True, WHITE, ), (680, 515))
    else:
        screen.blit(pygame.font.SysFont("Times New Roman", 30).render("DIFFICULTY HARD", True, WHITE, ), (680, 515))
    screen.blit(pygame.font.SysFont("Times New Roman", 30).render("BACK", True, WHITE, ), (765, 665))


def deathScreen():
    """
    Draws all the boxes and text for the death screen
    :return:
    """
    global GAME_STATE
    screen.fill(DARK_GREEN)
    pygame.draw.rect(screen, GREY, options_button)
    pygame.draw.rect(screen, GREY, exit_button)
    screen.blit(pygame.font.SysFont("Times New Roman", 30).render("YOU DIED", True, WHITE, ), (750, 200))
    screen.blit(pygame.font.SysFont("Times New Roman", 30).render("MAIN MENU", True, WHITE, ), (730, 515))
    screen.blit(pygame.font.SysFont("Times New Roman", 30).render("EXIT", True, WHITE, ), (765, 665))


class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, max_health, speed):
        """
        Super class for player and enemy
        :param x: Objects x coordinate
        :param y: Objects y coordinate
        :param max_health: Objects maximum/starting health
        :param speed: Integer value the speed of the object
        """
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.scale = 1
        self.speed = speed
        self.max_health = max_health
        self.health = max_health
        self.img = pygame.image.load(os.path.join("Sprites", "Soldier 1", "Idle.png")).convert_alpha()
        self.img = pygame.image.load("_idle.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.img, self.scale * 5)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.oGravity = -1.5
        self.Gravity = -1.5
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
        self.camera_offset_x = 0
        self.collision = False
        if len(self.ammoVisual) < 5:
            for i in range(5 - len(self.bullets)):
                self.ammoVisual.append((1040, -150 - 10 * (len(self.ammoVisual))))

    def updateY(self, g):
        """
        Changes the objects y position
        :param g: Float which controls the upwards acceleration
        :return:
        """
        self.y = self.y + g
        rect = self.img.get_rect()
        rect.center = (self.x, self.y)
        self.rect.center = (self.x, self.y)

    def getHealth(self) -> int:
        """
        Returns objects health
        :return:
        """
        return self.health

    def updateHealth(self, damage):
        """
        Decreases objects health by the parameter damage
        :param damage: Float which is the amount health decreases by
        :return:
        """
        self.health = self.health - damage

    def yVelocity(self):
        """
        Manages the Y velocity of the object
        :return:
        """
        self.vel = self.vel - self.Gravity
        self.updateY(self.vel)

    def collisionCheck3(self, block):
        if self.rect.colliderect(block):
            self.vel = 0
            self.Gravity = 0
            self.collision = True
            return False
        else:
            self.collision = False
            return True

    def wallCollision(self, tile):
        tile.rect.collidepoint((self.x + 45), (self.y + 30))
        pygame.draw.circle(screen, RED, (self.x + 45, self.y + 30), 5)
        print("wall collision")

    def bulletManage(self):
        """
        Manages all the bullets on screen that came from this object
        :return:
        """
        for soldierBullet in self.bullets:
            soldierBullet.draw()

            if soldierBullet.hitCheck(self.rect, 0):
                print("hit")
                self.bullets.pop(self.bullets.index(soldierBullet))
            if player1.x + 900 > soldierBullet.x > player1.x - 700:
                soldierBullet.x += soldierBullet.speed
            else:
                self.ammoVisual.append((1040, -150 - 10 * (len(self.ammoVisual))))
                if len(self.ammoVisual) > 0:
                    self.bullets.pop(self.bullets.index(soldierBullet))

        for i in self.ammoVisual:
            # print(len(self.ammoVisual))
            screen.blit(self.ammunition, i)
            # screen.blit(i, (1040, -200 + 10 * (len(self.ammoVisual))))
            # pygame.draw.circle(screen, RED, (1040, 0 + 10 * (len(self.ammoVisual))), 7)

        # self.rect = get_image(player_running, i, 128, 67, 3, WHITE)


class Player(Soldier):
    def __init__(self, x, y):
        """
        Subclass of soldier which has methods which are unique to this class
        :param x: Objects x coordinate
        :param y: Objects y coordinate
        """
        super().__init__(x, y, 100, 1)
        self.c_time = None
        self.bar = None
        self.scale = 3

    def updateX(self, L, R):
        """
        Updates the objects x position
        :param L: True if facing Left
        :param R: True if facing Right
        :return:
        """
        if L:
            self.camera_offset_x -= 10
        if R:
            self.camera_offset_x += 10

    def UI(self):
        """
        Draws and updates the players health bar and ammunition count at the top of the screen
        :return:
        """
        # Health Bar
        pygame.draw.rect(screen, SILVER, (10, 40, 400, 40), 20)
        pygame.draw.rect(screen, BLACK, (5, 35, 410, 50), 5)
        self.bar = pygame.Rect(10, 40, 4 * self.health, 40)
        pygame.draw.rect(screen, RED, self.bar, 50)
        health_count = health.render(("Health:" + str(player1.health)), True, (0, 0, 0))
        screen.blit(health_count, (10, 35))
        # Ammunition count
        pygame.draw.rect(screen, (70, 70, 70), (1350, 0, 400, 100))
        pygame.draw.rect(screen, BLACK, (1360, 15, 45, 80))
        ammunition = ammo.render(("Ammo:" + str(5 - len(self.bullets)) + "/" + str(self.maxBullets)), True,
                                 (0, 0, 0))
        screen.blit(ammunition, (1420, 35))

    def shoot(self):
        """
        Responsible for creating bullets and changing the players state when firing
        :return:
        """
        if len(self.ammoVisual) > 0:
            self.ammoVisual.pop()
        self.state = "firing"
        if len(self.bullets) < self.maxBullets:
            pygame.mixer.Sound.play(shoot)
            self.bullets.append(
                Projectile((self.rect.center[0], self.rect.center[1] - 30), 20, self.direction, RED))

    def animationManage(self):
        """
        Runs specific animations depending on the current state of the player
        :return:
        """
        global animation_list
        self.c_time = pygame.time.get_ticks()
        if self.state == "idle":
            animation_steps = 4
            animation_list = []
            if self.direction == "RIGHT":
                for i in range(animation_steps):
                    animation_list.append(get_image(player_idle_right, i, 128, 67, self.scale, WHITE))
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

            pass

        screen.blit((animation_list[self.frame]), (self.x - 180, self.y - 100))


class Enemy(Soldier):
    def __init__(self, x, y, ):
        """
        Subclass which holds the unique methods and attribute for the non-playable enemy
        :param x: Objects x coordinate
        :param y: Objects y coordinate
        """
        super().__init__(x, y, 100, 0.3)
        self.bar = None
        self.c_time = None
        self.scale = 3
        self.t = pygame.time.get_ticks()
        self.T = self.t + 500
        self.maxBullets = 1
        self.move = random.randint(-1, 1)
        self.seen = False  # private attribute which outputs True if the player has been seen by the enemy
        self.shoot_cooldown = 400
        self.move_cooldown = random.randint(400, 600)
        self.l_up = pygame.time.get_ticks()
        self.last_up = pygame.time.get_ticks()
        # self.x = player1.camera_offset_x + self.x
        # self.rect.center = (self.x, self.y)

    def healthBar(self):
        """
        Draws and updates a health bar over the object
        :return:
        """
        pygame.draw.rect(screen, SILVER, (self.x - 45 - player1.camera_offset_x, self.y - 120, 100, 5), 20)
        pygame.draw.rect(screen, BLACK, (self.x - 50 - player1.camera_offset_x, self.y - 125, 110, 15), 5)
        self.bar = pygame.Rect(self.x - 45 - player1.camera_offset_x, self.y - 120, 1 * self.health, 5)
        pygame.draw.rect(screen, RED, self.bar, 50)

    def camera(self):
        pass
        # if self.state == "idle" or self.state == "firing":
        #     self.x = -player1.camera_offset_x
        # self.rect.center = (self.x, self.y)

    def updateX(self, L, R):
        """
        Updates the objects x position
        :param L: True if facing Left
        :param R: True if facing Right
        :return:
        """
        if L:
            self.x = self.x + -10 * self.speed
            rect = self.img.get_rect()
            # rect.center = (self.x, self.y)
            self.rect.center = (self.x, self.y)

        if R:
            self.x = self.x + 10 * self.speed
            rect = self.img.get_rect()
            # rect.center = (self.x, self.y)
            self.rect.center = (self.x, self.y)

    def shoot(self):
        """
        Responsible for creating bullets and changing the players state when firing
        :return:
        """
        self.state = "firing"
        if len(self.bullets) < self.maxBullets:
            pygame.mixer.Sound.play(shoot)
            self.bullets.append(
                Projectile((self.rect.center[0] - player1.camera_offset_x, self.rect.center[1] - 30), 20,
                           self.direction, RED))

    def vision(self, target_x, target_y):
        """
        Checks if the object has seen the enemy within a certain range
        :param target_x: Targets(player) x coordinate
        :param target_y: Targets(player) y coordinate
        :return: True if the player has been seen and is in range
        """
        x = self.x
        if self.direction == "RIGHT":
            for i in range(500):
                if target_x - 50 < self.x - player1.camera_offset_x + i < target_x + 50:
                    # print("great success")
                    return True
        if self.direction == "LEFT":
            for i in range(500):
                if target_x - 50 < self.x - player1.camera_offset_x - i < target_x + 50:
                    # print("great success")
                    return True
            # else:
            #     return False
        self.x = x

    def movement(self):
        """
        Responsible for the random movement of the enemy
        :return:
        """
        self.c_time = pygame.time.get_ticks()
        if self.move == 1:
            self.updateX(0, 1)
            self.state = "walking"
            self.direction = "RIGHT"
            # print("c", self.c_time)
            # print("u", self.last_update)
            if self.c_time - self.last_up >= self.move_cooldown:
                self.move = 0
                self.last_up = self.c_time
        # print(self.move)
        if self.move == -1:
            self.updateX(1, 0)
            self.state = "walking"
            self.direction = "LEFT"
            # print("c", self.c_time)
            # print("u", self.last_update)
            if self.c_time - self.last_up >= self.move_cooldown:
                self.move = 0
                self.last_up = self.c_time
        if self.move == 0:
            self.state = "idle"
            if self.c_time - self.last_up >= self.move_cooldown + 700:
                self.move = random.randint(-1, 1)
                self.last_up = self.c_time

    def AI(self):
        """
        Links together previous methods in order to make a working AI
        :return:
        """
        c_time = pygame.time.get_ticks()
        self.movement()
        if self.vision(player1.x, player1.y):
            self.seen = True
            self.move = 0
            # print("c", c_time)
            # print("u", self.l_up)
            self.state = "firing"
            if c_time - self.l_up >= self.shoot_cooldown:
                self.l_up = c_time
                enemy.shoot()

        if self.seen:
            if not self.vision(player1.x, player1.y):
                if self.x - player1.camera_offset_x - player1.x < 0:
                    self.move = 1
                else:
                    self.move = -1
            else:
                self.move = 0

    def animationManage(self):
        """
        Runs specific animations depending on the current state of the player
        :return:
        """
        global animation_list
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
                    animation_list.append(get_image(enemy_walk_left, i, 128, 65, 3, WHITE))
                if self.c_time - self.last_update >= self.animation_cooldown:
                    self.frame += 1
                    if self.frame >= len(animation_list):
                        self.frame = 0
                    self.last_update = self.c_time

        if self.state == "null":
            pass

        # self.rect.center = (self.x - player1.camera_offset_x , self.y)
        screen.blit((animation_list[self.frame]), (self.x - 180 - player1.camera_offset_x, self.y - 100))


test = tiles(1000, 500)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, center, speed, direction, colour):
        """
        Holds the methods and attributes for bullets in the game
        :param center: The center of the object which is shooting
        :param speed: The speed of the bullet
        :param direction: The direction the bullet will go
        :param colour: The colour of the bullet
        """
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

    def hitCheck(self, targetCoords, x):
        """
        Checks if the bullet is impacting on the target coordinates
        :param targetCoords: Targets rect
        :return: True if bullet is on the target coordinates
        """
        # print(targetCoords[0])
        # print(self.x)
        if targetCoords[0] <= self.x + x <= (targetCoords[2] + targetCoords[0]) and targetCoords[1] <= self.y <= (
                targetCoords[1] + targetCoords[3]):
            return True
        else:
            return False

    def draw(self):
        """
        Draws the bullet
        :return:
        """
        pygame.draw.circle(screen, self.colour, (self.x, self.y), 7)


# def draw(x1, y1, x2, y2, width):
#     pygame.draw.rect(screen, GREEN, (x1, y1, x2, y2), width)


player1 = Player(700, 200)

Jump = False

# bullets = []
enemies = []
update1 = pygame.time.get_ticks() + 200
clock = pygame.time.Clock()
while True:
    if not player1.collision:
        player1.updateX(moveLeft, moveRight)

    # elif 0 >= player1.x:
    #     player1.updateX(0, moveRight)
    # elif 0 <= player1.x:
    #     player1.updateX(moveLeft, 0)
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

    if Jump and player1.Gravity == 0:
        player1.vel = -30
        Jump = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

        if GAME_STATE != "playing":
            menuControls()

        if GAME_STATE == "playing":
            if event.type == pygame.KEYDOWN:
                # Checks for keyboard inputs
                if event.key == pygame.K_a:
                    if not player1.collision:
                        moveLeft = True
                        pygame.mixer.Sound.play(walking)
                        player1.direction = "LEFT"
                        player1.state = "running"
                if event.key == pygame.K_d:
                    if not player1.collision:
                        pygame.mixer.Sound.play(walking)
                        moveRight = True
                        player1.state = "running"
                        player1.direction = "RIGHT"
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    Jump = True
                if event.key == pygame.K_j:
                    player1.shoot()
                if event.key == pygame.K_i:
                    # print("c", player1.camera_offset_x)
                    genBlock(player1.camera_offset_x)
                    print(blocks)
                if event.key == pygame.K_l:
                    # enemies.append(Enemy(random.randint(30, 1570), 300, 5))
                    enemies.append(Enemy(1000, 324))
                if event.key == pygame.K_p:
                    GAME_STATE = "options"
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

    # Checking game states
    if GAME_STATE == "menu":
        mainMenu()
    if GAME_STATE == "options":
        options()
    if GAME_STATE == "death":
        deathScreen()

    if GAME_STATE == "playing":
        loadBack(1)
        if player1.getHealth() <= 0:
            GAME_STATE = "death"
            player1 = Player(700, 200)
            enemies.clear()
        player1.animationManage()
        for enemy in enemies:
            # enemy.x = player1.camera_offset_x + 800
            print(enemy.x)
            enemy.camera()
            enemy.yVelocity()
            for block in blocks:
                enemy.collisionCheck3(block)
            enemy.animationManage()
            enemy.healthBar()
            enemy.AI()
            enemy.bulletManage()
            enemy.rect.center = (enemy.x - player1.camera_offset_x, enemy.y)
            # if 0 >= enemy.x:
            #     enemy.move = 1
            # elif 1600 <= enemy.x:
            #     enemy.move = -1
            for bullet in enemy.bullets:
                # Checks each enemy bullet to see if it hits the player
                if bullet.hitCheck(player1.rect, 0):
                    if difficulty == "easy":
                        player1.updateHealth(15)
                    elif difficulty == "hard":
                        player1.updateHealth(22)
                    print("hit")
                    enemy.bullets.pop(enemy.bullets.index(bullet))
            for bullet in player1.bullets:
                if bullet.hitCheck(enemy.rect, 0):
                    enemy.updateHealth(25)
                    if player1.direction == "RIGHT":
                        enemy.move = -1
                    elif player1.direction == "LEFT":
                        enemy.move = 1
                    player1.ammoVisual.append((1040, -150 - 10 * (len(player1.ammoVisual))))
                    player1.bullets.pop(player1.bullets.index(bullet))
            # Removes enemies if they reach 0 or below health
            if enemy.getHealth() <= 0:
                if enemy.c_time - update1 >= 2000:
                    enemies.pop(enemies.index(enemy))
        if not player1.collision:
            player1.yVelocity()
            player1.Gravity = player1.oGravity
        player1.UI()
        player1.bulletManage()
        # print(blockRect)
        # player1.collisionCheck2(blockRect)
        for block in blocks:
            player1.collisionCheck3(block)
            # player1.wallCollision(block)
            # print(block.rect)
            # if block.rect.collidepoint(player1.x + 45, player1.y + 30):
            #     print("col")
        # for y in blockRect:
        #     pygame.draw.rect(screen, RED, y)
    # pygame.time.set_timer()
    # player1.healthBar()
    # player1.ammoCounter()
    # print(player1.x)
    # print(player1.rect)
    # pygame.draw.rect(screen, RED, (100- player1.camera_offset_x,600,100, 100))
    # pygame.draw.rect(screen, RED, player1.rect)
    # camera_offset_x = 1600 // 2 - player1.x - 50 // 2
    # print(player1.camera_offset_x)
    pygame.display.flip()
    clock.tick(60)
    # print(clock.get_fps())

# pygame.quit()
