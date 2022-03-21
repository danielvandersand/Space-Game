import pygame
import os
pygame.font.init()
pygame.mixer.init()

from pygame.constants import K_LCTRL, K_RCTRL

width, height = 900, 500
WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
gray = (128, 128, 128)
black = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(445, 0, 10, 500)



HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

fps = 60
vel = 3
max_bullets = 7
bullet_vel = 5


YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


yellow_spaceship_image = pygame.image.load(
    os.path.join('Assets','spaceship_yellow.png'))

yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(
    yellow_spaceship_image, (55, 40)), 90)

red_spaceship_image = pygame.image.load(
    os.path.join('Assets','spaceship_red.png'))

red_spaceship = pygame.transform.rotate(pygame.transform.scale(
    red_spaceship_image, (55, 40)), 270)



def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.fill((gray))
    pygame.draw.rect(WIN, black, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, black)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, black)

    WIN.blit(red_health_text, (width - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))


    WIN.blit(yellow_spaceship, (yellow.x, yellow.y))
    WIN.blit(red_spaceship, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
        if keys_pressed[pygame.K_a] and yellow.x - vel > 0: # left key
            yellow.x -= vel
        if keys_pressed[pygame.K_d] and yellow.x + vel + yellow.width < BORDER.x: # right key
            yellow.x += vel
        if keys_pressed[pygame.K_w] and yellow.y - vel > 0: # up key
            yellow.y -= vel
        if keys_pressed[pygame.K_s] and yellow.y + vel + yellow.height < height - 15: # down key
            yellow.y += vel

def red_handle_movement(keys_pressed, red):
            # red spaceship
        if keys_pressed[pygame.K_LEFT] and red.x - vel > BORDER.x + BORDER.width: # left key
            red.x -= vel
        if keys_pressed[pygame.K_RIGHT] and red.x + vel + red.width < width: # right key
            red.x += vel
        if keys_pressed[pygame.K_UP] and red.y - vel > 0: # up key
            red.y -= vel
        if keys_pressed[pygame.K_DOWN] and red.y + vel + red.height < height - 15: # down key
            red.y += vel

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > width:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, black)
    WIN.blit(draw_text, (
        width/2 - draw_text.get_width()/2, height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():

    red = pygame.Rect(800, 300, 55, 40)
    yellow = pygame.Rect(100, 300, 55, 40)

    yellow_bullets = []
    red_bullets = []
    yellow_health = 10
    red_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < max_bullets:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)


                if event.key == pygame.K_RCTRL and len(red_bullets) < max_bullets:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)

        

            if event.type == RED_HIT:
                red_health -= 1


            if event.type == YELLOW_HIT:
                yellow_health -= 1

        winner_text = ""
        if red_health <= 0:
            winner_text = "yellow wins!"
        
        if yellow_health <= 0:
            winner_text = "red wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)


        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()

if __name__ == "__main__":
    main()