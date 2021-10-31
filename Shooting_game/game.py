import os

import pygame

pygame.font.init()
pygame.mixer.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting game!")
BACKGROUND = pygame.transform.scale(
    pygame.image.load(os.path.join("Resources", "background_1.png")), (WIDTH, HEIGHT)
)

BOW_EFFECT_LEFT = pygame.mixer.Sound("Resources/bow_shoot_left.mp3")
BOW_EFFECT_RIGHT = pygame.mixer.Sound("Resources/bow_shoot_right.mp3")
ARROW_IMPACT = pygame.mixer.Sound("Resources/arrow_impact.mp3")

HEALTH_FONT = pygame.font.SysFont("comicsans", 30)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

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
RIGHT_ARROW_IMAGE = pygame.image.load(os.path.join("Resources", "right_arrow.png")).convert_alpha()
LEFT_ARROW_IMAGE = pygame.image.load(os.path.join("Resources", "left_arrow.png")).convert_alpha()


def draw_window(left, right, red_bullets, blue_bullets, left_health, right_health):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    left_health_text = HEALTH_FONT.render("Health: " + str(left_health), 1, WHITE)
    right_health_text = HEALTH_FONT.render("Health: " + str(right_health), 1, WHITE)
    WIN.blit(left_health_text, (WIDTH - left_health_text.get_width() - 10, 10))
    WIN.blit(right_health_text, (10, 10))
    WIN.blit(LEFT_ARCHER, (left.x, left.y))
    WIN.blit(RIGHT_ARCHER, (right.x, right.y))

    for bullet in red_bullets:
        # pygame.draw.rect(WIN, RED, bullet)
        WIN.blit(RIGHT_ARROW_IMAGE, bullet)

    for bullet in blue_bullets:
        # pygame.draw.rect(WIN, BLUE, bullet)
        WIN.blit(LEFT_ARROW_IMAGE, bullet)

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


def draw_winner(winner_text):
    draw_text = WINNER_FONT.render(winner_text, 1, WHITE)
    WIN.blit(
        draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2)
    )
    pygame.display.update()
    pygame.time.delay(4000)


def main():
    left = pygame.Rect(0, HEIGHT / 2 - ARCHER_HEIGHT, ARCHER_WIDTH, ARCHER_HEIGHT / 2)
    right = pygame.Rect(
        WIDTH - ARCHER_WIDTH, HEIGHT / 2 - ARCHER_HEIGHT, ARCHER_WIDTH, ARCHER_HEIGHT / 2
    )

    red_bullets = []
    blue_bullets = []

    left_health = 10
    right_health = 10

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
                    bullet = pygame.Rect(left.x, left.y + left.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BOW_EFFECT_LEFT.play()
                if event.key == pygame.K_RCTRL and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(right.x, right.y + right.height // 2 - 2, 10, 5)
                    blue_bullets.append(bullet)
                    BOW_EFFECT_RIGHT.play()

            if event.type == LEFT_HIT:
                right_health -= 1
                ARROW_IMPACT.play()

            if event.type == RIGHT_HIT:
                left_health -= 1
                ARROW_IMPACT.play()

        winner_txt = ""
        if left_health <= 0:
            winner_txt = "Left Wins!"

        if right_health <= 0:
            winner_txt = "Right Wins!"

        if winner_txt != "":
            draw_winner(winner_txt)
            break

        keys_pressed = pygame.key.get_pressed()
        left_handle_movement(keys_pressed, left)
        right_handle_movement(keys_pressed, right)

        handle_bullets(red_bullets, blue_bullets, left, right)
        draw_window(left, right, red_bullets, blue_bullets, left_health, right_health)

    main()


if __name__ == "__main__":
    main()
