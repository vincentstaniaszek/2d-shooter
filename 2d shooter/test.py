import pygame
import sys

# Initialize Pygame
pygame.init()
pygame.display.set_caption("2D shooter")
surface = pygame.display.set_mode([1600, 900])
# Create a game surface
while True:
    surface.fill((43, 163, 212))

    # draw(100, 300, 1000, 100, 10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # if event.type == pygame.KEYDOWN:
        #     pygame.key.set_repeat(10, 2)
        #     if event.key == pygame.K_a:
        #         # player.updateX(-1)
        #     if event.key == pygame.K_d:
        #         # player.updateX(1)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # if event.key == pygame.K_SPACE:
            #     player.jump()

            if event.key == pygame.K_SPACE:
                print("pls")
                # player.jump()
        if event.type == pygame.KEYDOWN:

            # checking if key "A" was pressed
            if event.key == pygame.K_a:
                print("Key A has been pressed")

            # checking if key "J" was pressed
            if event.key == pygame.K_j:
                print("Key J has been pressed")

            # checking if key "P" was pressed
            if event.key == pygame.K_p:
                print("Key P has been pressed")

            # checking if key "M" was pressed
            if event.key == pygame.K_m:
                print("Key M has been pressed")
        # if event.type == pygame.

    # surface.blit(player.image, player.rect)

    # pygame.display.update()
    pygame.display.flip()

pygame.quit()
