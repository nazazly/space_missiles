import pygame
import time
import random
pygame.mixer.init(44100, 16, 2, 4096)
pygame.font.init()

# Create game screen size

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Missles")

BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))

# Use constants for the scale of game objects

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 10
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

# Play background music

pygame.mixer.music.load("start.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

FONT = pygame.font.SysFont("Times New Roman", 30)

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "red", player)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    # For collision. Add "stars" 2000ms
    star_add_increment = 2000
    
    # When to add the next "star"
    star_count = 0

    stars = []
    hit = False

    while run:
        #Return new star after each tick
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                
                # Negative so that the "star" goes down the y axis
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
                
        keys = pygame.key.get_pressed()
        # Code for left arrow key. Limit the player movement within the console
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:

            #subtract x coordinate to bring it closer to 0 (moving to the left)
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:

            #add x coordinate to bring it closer to right
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You lost!", 1 ,"white")

            # Adjusting the text to appear in the middle of the screen
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(3000)
            break

        draw(player, elapsed_time, stars)
    
    pygame.quit()

if __name__ == "__main__":
    main()