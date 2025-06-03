#space invaders game

import pygame 
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Ship setup
ship_width, ship_height = 50, 30
ship_x, ship_y = WIDTH // 2, HEIGHT - 60
ship_speed = 5

# Ship lives
lives = 3
font = pygame.font.SysFont(None, 36)

# Bullet setup
bullets = []
bullet_width, bullet_height = 5, 10
bullet_speed = 7
BULLET_COLOR = (0, 255, 0)

#Import enemy ship image
enemy_image = pygame.image.load("spaceship.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (40, 40))
enemy_x = 100
enemy_y = 100

# Multiple Enemies setup
enemy_width, enemy_height = 40, 30
enemies = [
    {"x": 100, "y": 100, "dir": 1},
    {"x": 300, "y": 100, "dir": 1},
    {"x": 500, "y": 100, "dir": 1},
]
enemy_speed = 3


# Enemy bullets
enemy_bullets = []
enemy_bullet_width, enemy_bullet_height = 5, 10
enemy_bullet_speed = 5
enemy_fire_delay = 60  # frames between shots
enemy_fire_timer = 0

# Fonts
font = pygame.font.SysFont(None, 36)

#Draw Start Button function
def draw_start_button():
    button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 20, 150, 50)
    pygame.draw.rect(screen, (0, 0, 255), button_rect)
    text = font.render("Start", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 45, HEIGHT // 2 + 30))

#creates screen to start game function
def show_start_screen():
    screen.fill(BLACK)
    title_text = font.render("Push button to start Game", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - 180, HEIGHT // 2 - 40))
    draw_start_button()
    pygame.display.flip()
    wait_for_restart()


#Draw restart Button function
def draw_restart_button():
    button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 20, 150, 50)
    pygame.draw.rect(screen, (0, 0, 255), button_rect)
    text = font.render("Restart", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 45, HEIGHT // 2 + 30))

#restart function
def wait_for_restart():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 20, 150, 50)
                if button_rect.collidepoint(mouse_pos):
                    return  # exits wait and restarts game

# Show start screen when game is loaded
show_start_screen()

#Game loop
def game_loop():
    # Game state
    ship_x, ship_y = WIDTH // 2, HEIGHT - 60
    lives = 3

    bullets = []
    enemy_bullets = []
    enemy_fire_timer = 0

    enemies = [
        {"x": 100, "y": 100, "dir": 1},
        {"x": 300, "y": 100, "dir": 1},
        {"x": 500, "y": 100, "dir": 1},
    ]

    running = True
    clock = pygame.time.Clock()


    while running:
        clock.tick(60)  # 60 frames per second

        # Draw everything
        screen.fill(BLACK)

        # Create enemies
        for enemy in enemies:
            screen.blit(enemy_image, (enemy["x"], enemy["y"]))
    
        # Draw enemy bullets
        for bullet in enemy_bullets:
            pygame.draw.rect(screen, (255, 255, 0), (bullet[0], bullet[1], enemy_bullet_width, enemy_bullet_height))

        # draw ship
        pygame.draw.rect(screen, WHITE, (ship_x, ship_y, ship_width, ship_height))

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_x = ship_x + ship_width // 2 - bullet_width // 2
                    bullet_y = ship_y
                    bullets.append([bullet_x, bullet_y])
    
        # Move enemy
        for enemy in enemies:
            enemy["x"] += enemy["dir"] * enemy_speed
            if enemy["x"] <= 0 or enemy["x"] >= WIDTH - enemy_width:
                enemy["dir"] *= -1

        # Enemy fires bullet periodically (random)
        enemy_fire_timer += 1
        if enemy_fire_timer >= enemy_fire_delay:
            enemy_fire_timer = 0
            firing_enemy = random.choice(enemies)
            bullet_x = firing_enemy["x"] + enemy_width // 2 - enemy_bullet_width // 2
            bullet_y = firing_enemy["y"] + enemy_height
            enemy_bullets.append([bullet_x, bullet_y])

        # Move enemy bullets
        for bullet in enemy_bullets[:]:
            bullet[1] += enemy_bullet_speed
            if bullet[1] > HEIGHT:
                enemy_bullets.remove(bullet)

        # Move bullets
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, BULLET_COLOR, (bullet[0], bullet[1], bullet_width, bullet_height))

        #bullet-enemy collisions
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if (enemy["x"] < bullet[0] < enemy["x"] + enemy_width and
                    enemy["y"] < bullet[1] < enemy["y"] + enemy_height):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break
    
        #Bullet-ship collisions
        for bullet in enemy_bullets[:]:
            if (ship_x < bullet[0] < ship_x + ship_width and
                ship_y < bullet[1] < ship_y + ship_height):
                enemy_bullets.remove(bullet)
                lives -= 1
                # Hide ship briefly and reposition
                ship_x, ship_y = WIDTH // 2, HEIGHT - 60
                pygame.time.delay(500)  # 0.5 second pause
                break
 
        # Movement keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and ship_x > 0:
            ship_x -= ship_speed
        if keys[pygame.K_d] and ship_x < WIDTH - ship_width:
            ship_x += ship_speed


        # Show lives
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (10, 10))

        #If lives run out
        if lives <= 0:
            screen.fill(BLACK)
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False
    
        # WIN condition check
        if not enemies:
            screen.fill(BLACK)
            win_text = font.render("YOU WIN!", True, (0, 255, 0))
            screen.blit(win_text, (WIDTH // 2 - 80, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False


        #display
        pygame.display.flip()


# Start the game and allow restart loop
while True:
    game_loop()

    screen.fill(BLACK)
    game_over_text = font.render("Click Restart to Play Again", True, (255, 0, 0))
    screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 40))
    draw_restart_button()
    pygame.display.flip()
    wait_for_restart()


pygame.quit()
sys.exit()

