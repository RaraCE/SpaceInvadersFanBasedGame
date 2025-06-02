#space invaders game
# as extra credit - create a small ML program that will learn from the player's choices

import pygame # type: ignore
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


# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # 60 frames per second

    # Draw everything
    screen.fill(BLACK)

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, (255, 0, 0), (enemy["x"], enemy["y"], enemy_width, enemy_height))
    
    # Draw enemy bullets
    for bullet in enemy_bullets:
        pygame.draw.rect(screen, (255, 255, 0), (bullet[0], bullet[1], enemy_bullet_width, enemy_bullet_height))

    # draw ship
    pygame.draw.rect(screen, WHITE, (ship_x, ship_y, ship_width, ship_height))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                #print("Bullet fired!")
                # Fire a bullet from the center-top of the ship
                bullet_x = ship_x + ship_width // 2 - bullet_width // 2
                bullet_y = ship_y
                bullets.append([bullet_x, bullet_y])
        if event.type == pygame.QUIT:
            running = False
    
    # Move enemy
    for enemy in enemies:
        enemy["x"] += enemy["dir"] * enemy_speed
        if enemy["x"] <= 0 or enemy["x"] >= WIDTH - enemy_width:
            enemy["dir"] *= -1

    # Enemy fires bullet periodically (random enemy)
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

    for bullet in bullets[:]:
        for enemy in enemies:
            if (enemy["x"] < bullet[0] < enemy["x"] + enemy_width and
                enemy["y"] < bullet[1] < enemy["y"] + enemy_height):
                bullets.remove(bullet)
                # Respawn enemy at a new random x
                enemy["x"] = random.randint(0, WIDTH - enemy_width)
                enemy["y"] = 100
                break
            # Respawn enemy at a new position
    
    # Check if enemy bullet hits ship
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
    if keys[pygame.K_w] and ship_y > 0:
        ship_y -= ship_speed
    if keys[pygame.K_s] and ship_y < HEIGHT - ship_height:
        ship_y += ship_speed
    if keys[pygame.K_a] and ship_x > 0:
        ship_x -= ship_speed
    if keys[pygame.K_d] and ship_x < WIDTH - ship_width:
        ship_x += ship_speed


    # Show lives
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (10, 10))

    if lives <= 0:
        screen.fill(BLACK)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False


    #display
    pygame.display.flip()



pygame.quit()
sys.exit()

