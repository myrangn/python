import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Game variables
GRAVITY = 0.25
BIRD_JUMP = -6.5
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds
PIPE_SPEED = 3

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

# Fonts
FONT = pygame.font.SysFont("Arial", 32)

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.radius = 20
        self.velocity = 0

    def flap(self):
        self.velocity = BIRD_JUMP

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self, surface):
        # A simple bird shape
        body_rect = pygame.Rect(self.x - self.radius, self.y - (self.radius * 0.75), self.radius * 2, self.radius * 1.5)
        pygame.draw.ellipse(surface, YELLOW, body_rect)
        
        # Wing
        wing_rect = pygame.Rect(self.x - 10, self.y, 20, 12)
        pygame.draw.ellipse(surface, YELLOW, wing_rect)
        pygame.draw.ellipse(surface, BLACK, wing_rect, 1) # outline for wing

        # Eye
        pygame.draw.circle(surface, BLACK, (int(self.x + 7), int(self.y - 5)), 3)

        # Beak
        beak_points = [(self.x + self.radius, self.y), (self.x + self.radius + 10, self.y - 3), (self.x + self.radius + 10, self.y + 3)]
        pygame.draw.polygon(surface, ORANGE, beak_points)

    def get_rect(self):
        # Adjust the bounding box to be a bit tighter and account for the beak
        return pygame.Rect(self.x - self.radius, self.y - (self.radius * 0.75), self.radius * 2 + 10, self.radius * 1.5)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 60
        self.top_height = random.randint(50, HEIGHT - PIPE_GAP - 100)
        self.bottom_height = HEIGHT - self.top_height - PIPE_GAP

    def move(self):
        self.x -= PIPE_SPEED

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(surface, GREEN, (self.x, HEIGHT - self.bottom_height, self.width, self.bottom_height))

    def get_top_rect(self):
        return pygame.Rect(self.x, 0, self.width, self.top_height)

    def get_bottom_rect(self):
        return pygame.Rect(self.x, HEIGHT - self.bottom_height, self.width, self.bottom_height)

def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = []
    score = 0
    running = True
    last_pipe = pygame.time.get_ticks()
    game_over = False

    while running:
        clock.tick(60)
        SCREEN.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.flap()
                if event.key == pygame.K_r and game_over:
                    main()
                    return

        if not game_over:
            bird.move()

            # Add new pipes
            now = pygame.time.get_ticks()
            if now - last_pipe > PIPE_FREQUENCY:
                pipes.append(Pipe(WIDTH))
                last_pipe = now

            # Move and draw pipes
            for pipe in pipes:
                pipe.move()
                pipe.draw(SCREEN)

            # Remove off-screen pipes and update score
            pipes = [pipe for pipe in pipes if pipe.x + pipe.width > 0]
            for pipe in pipes:
                if pipe.x + pipe.width < bird.x and not hasattr(pipe, 'scored'):
                    score += 1
                    pipe.scored = True

            # Draw bird
            bird.draw(SCREEN)

            # Collision detection
            bird_rect = bird.get_rect()
            if bird.y - bird.radius <= 0 or bird.y + bird.radius >= HEIGHT:
                game_over = True
            for pipe in pipes:
                if bird_rect.colliderect(pipe.get_top_rect()) or bird_rect.colliderect(pipe.get_bottom_rect()):
                    game_over = True

            # Draw score
            score_text = FONT.render(str(score), True, WHITE)
            SCREEN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 30))
        else:
            # Game over screen
            over_text = FONT.render("Game Over!", True, WHITE)
            restart_text = FONT.render("Press R to Restart", True, WHITE)
            SCREEN.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 40))
            SCREEN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()