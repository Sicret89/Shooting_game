import os

import pygame

os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting game!")

WHITE = (255, 255, 255)
FPS = 60
ARCHER_WIDTH, ARCHER_HEIGHT = 40, 45

LEFT_ARCHER_IMAGE = pygame.image.load(os.path.join("Resources", "left_archer.png")).convert()
LEFT_ARCHER = pygame.transform.rotate(
    pygame.transform.scale(LEFT_ARCHER_IMAGE, (ARCHER_WIDTH, ARCHER_HEIGHT)), 0
)
RIGHT_ARCHER_IMAGE = pygame.image.load(os.path.join("Resources", "right_archer.png")).convert()
RIGHT_ARCHER = pygame.transform.rotate(
    pygame.transform.scale(RIGHT_ARCHER_IMAGE, (ARCHER_WIDTH, ARCHER_HEIGHT)), 0
)


def draw_window():
    WIN.fill((WHITE))
    WIN.blit(LEFT_ARCHER, (300, 100))
    WIN.blit(RIGHT_ARCHER, (500, 100))
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()

    pygame.quit()


if __name__ == "__main__":
    main()
