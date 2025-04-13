import pygame
import numpy as np
import math

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SPACING = 20  # Spacing for the vector field grid
PARTICLE_RADIUS = 5
PARTICLE_COLOR = (255, 0, 0)
VECTOR_COLOR = (0, 0, 255)
BACKGROUND_COLOR = (0, 0, 0)
TIME_STEP = 0.1  # Numerical integration time step

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle in a Vector Field")
clock = pygame.time.Clock()

# Vector field defined by a differential equation
def vector_field(x, y):
    """
    Define the vector field: dx/dt = f(x, y), dy/dt = g(x, y)
    Example: Rotational field
    """
    f = x - x*y   # dx/dt = -y
    g = x*y - y   # dy/dt = x
    return np.array([f, g])

def draw_vector_field():
    """Draw arrows representing the vector field at grid points."""
    for x in range(0, WIDTH, GRID_SPACING):
        for y in range(0, HEIGHT, GRID_SPACING):
            # Calculate vector direction
            vx, vy = vector_field((x - WIDTH // 2) / 100, -(y - HEIGHT // 2) / 100)
            # Scale and normalize vector for drawing
            mag = np.hypot(vx, vy)
            if mag == 0: continue
            vx, vy = vx / mag * GRID_SPACING * 0.4, -vy / mag * GRID_SPACING * 0.4
            # Draw vector as an arrow
            pygame.draw.line(screen, VECTOR_COLOR, (x, y), (x + vx, y + vy), 2)
            pygame.draw.circle(screen, VECTOR_COLOR, (x + int(vx), y + int(vy)), 2)

class Particle:
    """A particle that moves according to the vector field."""
    def __init__(self, x, y):
        self.position = np.array([x, y], dtype=float)

    def update(self):
        # Get the vector field direction at the particle's position
        px, py = self.position
        vx, vy = vector_field((px - WIDTH // 2) / 100, -(py - HEIGHT // 2) / 100)
        velocity = np.array([vx, -vy])  # Invert Y-axis for Pygame's coordinate system
        # Update position using Euler's method
        self.position += TIME_STEP * velocity * 50  # Scale for visualization

    def draw(self):
        pygame.draw.circle(screen, PARTICLE_COLOR, self.position.astype(int), PARTICLE_RADIUS)

def main():
    # List to store all particles
    particles = []

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Add a new particle at the mouse position when space bar is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                particles.append(Particle(mouse_x, mouse_y))

        # Draw vector field
        draw_vector_field()

        # Update and draw all particles
        for particle in particles:
            particle.update()
            particle.draw()

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
