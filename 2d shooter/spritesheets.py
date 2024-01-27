from GUI import *
import pygame
# pygame.init()

BLACK = (0, 0, 0)

player_running = pygame.image.load(os.path.join("Sprites", "Soldier 1", "idle.png")).convert_alpha()


def get_image(sheet, frame, width, height, scale, colour):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colour)

    return image

frame_0 = get_image(player_running, 0, 128, 128, 3, BLACK)