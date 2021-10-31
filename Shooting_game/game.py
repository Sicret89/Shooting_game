import os

import pygame

os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting game!")
BACKGROUND = pygame.transform.scale(
    pygame.image.load(os.path.join("Resources", "background_1.png")), (WIDTH, HEIGHT)
)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 60
VEL = 5
BULLET_VEL = 8
MAX_BULLETS = 3
ARCHER_WIDTH, ARCHER_HEIGHT = 40, 45
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

LEFT_HIT = pygame.USEREVENT + 1
RIGHT_HIT = pygame.USEREVENT + 2

LEFT_ARCHER_IMAGE = pygame.image.load(os.path.join("Resources", "left_archer.png")).convert_alpha()
LEFT_ARCHER = pygame.transform.rotate(
    pygame.transform.scale(LEFT_ARCHER_IMAGE, (ARCHER_WIDTH, ARCHER_HEIGHT)), 0
)
RIGHT_ARCHER_IMAGE = pygame.image.load(
    os.path.join("Resources", "right_archer.png")
).convert_alpha()
RIGHT_ARCHER = pygame.transform.rotate(
    pygame.transform.scale(RIGHT_ARCHER_IMAGE, (ARCHER_WIDTH, ARCHER_HEIGHT)), 0
)


def draw_window(left, right, red_bullets, blue_bullets):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(LEFT_ARCHER, (left.x, left.y))
    WIN.blit(RIGHT_ARCHER, (right.x, right.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in blue_bullets:
        pygame.draw.rect(WIN, BLUE, bullet)

    pygame.display.update()


def left_handle_movement(keys_pressed, left):
    if keys_pressed[pygame.K_a] and left.x - VEL > 0:  # Moving Left
        left.x -= VEL
    if keys_pressed[pygame.K_d] and left.x + left.width < BORDER.x:  # Moving Right
        left.x += VEL
    if keys_pressed[pygame.K_w] and left.y - VEL > 0:  # Moving Up
        left.y -= VEL
    if keys_pressed[pygame.K_s] and left.y + left.height < HEIGHT:  # Moving Down
        left.y += VEL


def right_handle_movement(keys_pressed, right):
    if keys_pressed[pygame.K_LEFT] and right.x - VEL > BORDER.x - 5 + BORDER.width:  # Moving Left
        right.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and right.x + right.width < WIDTH - 5:  # Moving Right
        right.x += VEL
    if keys_pressed[pygame.K_UP] and right.y - VEL > 0:  # Moving Up
        right.y -= VEL
    if keys_pressed[pygame.K_DOWN] and right.y + right.height < HEIGHT:  # Moving Down
        right.y += VEL


def handle_bullets(red_bullets, blue_bullets, left, right):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if right.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RIGHT_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in blue_bullets:
        bullet.x -= BULLET_VEL
        if left.colliderect(bullet):
            pygame.event.post(pygame.event.Event(LEFT_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x < 0:
            blue_bullets.remove(bullet)


def main():
    left = pygame.Rect(100, 300, ARCHER_WIDTH, ARCHER_HEIGHT)
    right = pygame.Rect(500, 300, ARCHER_WIDTH, ARCHER_HEIGHT)

    red_bullets = []
    blue_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(left.x + left.width, left.y + left.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(right.x, right.y + right.height // 2 - 2, 10, 5)
                    blue_bullets.append(bullet)

        keys_pressed = pygame.key.get_pressed()
        left_handle_movement(keys_pressed, left)
        right_handle_movement(keys_pressed, right)

        handle_bullets(red_bullets, blue_bullets, left, right)
        draw_window(left, right, red_bullets, blue_bullets)

    main()


if __name__ == "__main__":
    main()
