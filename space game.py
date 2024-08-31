import pygame # type: ignore
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Collector")

# Load and scale assets dynamically
def load_and_scale_image(image_path, target_size):
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, target_size)
    return image

spaceship_image = load_and_scale_image('spaceship.png', (50, 50))
star_image = load_and_scale_image('star.png', (30, 30))
asteroid_image = load_and_scale_image('asteroid.png', (50, 50))
# Player setup
player_size = 50
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 2 * player_size
player_speed = 5

# Star setup
star_x = random.randint(0, SCREEN_WIDTH - 30)
star_y = random.randint(0, SCREEN_HEIGHT // 2)

# Asteroid setup
asteroid_speed = 3
asteroids = []

# Score setup
score = 0
high_score_file = "space_high_score.txt"

# Check if the high score file exists
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as file:
        high_score = int(file.read().strip())
else:
    high_score = 0

# Font setup
font = pygame.font.Font(None, 36)

# Particle effects
particles = []

def add_particles(x, y, color):
    for _ in range(5):  # Reduced the number of particles
        particles.append([x, y, random.randint(-3, 3), random.randint(-3, 3), color])

def draw_particles():
    for particle in particles:
        pygame.draw.circle(screen, particle[4], (particle[0], particle[1]), 3)
        particle[0] += particle[2]
        particle[1] += particle[3]
    particles[:] = [particle for particle in particles if 0 < particle[0] < SCREEN_WIDTH and 0 < particle[1] < SCREEN_HEIGHT and particle[2] != 0 and particle[3] != 0]

# Main game function
def main():
    global player_x, player_y, star_x, star_y, score, high_score
    clock = pygame.time.Clock()
    running = True
    game_active = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_active:
                    game_active = True
                    score = 0
                    player_x = SCREEN_WIDTH // 2
                    player_y = SCREEN_HEIGHT - 2 * player_size
                    star_x = random.randint(0, SCREEN_WIDTH - 30)
                    star_y = random.randint(0, SCREEN_HEIGHT // 2)
                    asteroids.clear()

        if game_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_size:
                player_x += player_speed
            if keys[pygame.K_UP] and player_y > 0:
                player_y -= player_speed
            if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - player_size:
                player_y += player_speed

            # Move asteroids
            if len(asteroids) < 5:
                asteroids.append([random.randint(0, SCREEN_WIDTH - 50), random.randint(-100, -50), asteroid_speed])

            for asteroid in asteroids:
                asteroid[1] += asteroid[2]
                if asteroid[1] > SCREEN_HEIGHT:
                    asteroids.remove(asteroid)

            # Check for collisions
            player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
            star_rect = pygame.Rect(star_x, star_y, 30, 30)
            if player_rect.colliderect(star_rect):
                score += 1
                add_particles(star_x, star_y, YELLOW)
                star_x = random.randint(0, SCREEN_WIDTH - 30)
                star_y = random.randint(0, SCREEN_HEIGHT // 2)

            collision = False
            for asteroid in asteroids:
                asteroid_rect = pygame.Rect(asteroid[0], asteroid[1], 50, 50)
                if player_rect.colliderect(asteroid_rect):
                    collision = True
                    add_particles(asteroid[0], asteroid[1], RED)
                    game_active = False

            if score > high_score:
                high_score = score
                with open(high_score_file, "w") as file:
                    file.write(str(high_score))

            # Clear screen
            screen.fill(BLACK)

            # Draw player
            screen.blit(spaceship_image, (player_x, player_y))

            # Draw star
            screen.blit(star_image, (star_x, star_y))

            # Draw asteroids
            for asteroid in asteroids:
                screen.blit(asteroid_image, (asteroid[0], asteroid[1]))

            # Draw particles
            draw_particles()

            # Draw score
            score_text = font.render(f"Score: {score}", True, WHITE)
            high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(high_score_text, (SCREEN_WIDTH - high_score_text.get_width() - 10, 10))

            if collision:
                # Display "Game Over" text and stop the game
                game_over_text = font.render("Game Over", True, RED)
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False
        else:
            # Start screen
            screen.fill(BLACK)
            start_text = font.render("Press SPACE to Start", True, WHITE)
            screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2))

        # Update screen
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
