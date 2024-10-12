import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screenWidth = 900
screenHeight = 750
floor_height = 700

# Colors
WHITE = (255, 255, 255)
MAROON = (128, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Verlet Simulation with Features")

# Gravity
gravity = pygame.Vector2(0, 180)
gravity_enabled = True

# Button dimensions and positions
button_width, button_height = 100, 40
add_button_rect = pygame.Rect(20, 20, button_width, button_height)
reset_button_rect = pygame.Rect(20, 70, button_width, button_height)
toggle_gravity_rect = pygame.Rect(20, 120, button_width, button_height)

# Helper function to create an anti-aliased circle
def draw_aa_circle(surface, color, center, radius):
    circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(circle_surface, color, (radius, radius), radius)
    return circle_surface

# Particle class using Verlet integration
class VerletObject:
    def __init__(self, x, y, radius, color):
        self.currentPosition = pygame.Vector2(x, y)
        self.oldPosition = pygame.Vector2(x, y)
        self.acceleration = pygame.Vector2(0, 0)
        self.radius = radius
        self.mass = math.pi * radius * radius * 0.01
        self.color = color

    def draw(self):
        circle_surface = draw_aa_circle(screen, self.color, (int(self.currentPosition.x), int(self.currentPosition.y)), self.radius)
        screen.blit(circle_surface, (int(self.currentPosition.x - self.radius), int(self.currentPosition.y - self.radius)))

    def update(self, dt):
        velocity = self.currentPosition - self.oldPosition
        self.oldPosition = self.currentPosition.copy()
        self.currentPosition += velocity + self.acceleration * dt * dt
        self.acceleration = pygame.Vector2(0, 0)
        self.handle_collisions(velocity)

    def apply_acceleration(self, acc):
        self.acceleration += acc

    def handle_collisions(self, velocity):
        if self.currentPosition.y > floor_height - self.radius:
            self.currentPosition.y = floor_height - self.radius
            self.oldPosition.y = self.currentPosition.y + velocity.y * 0.8
        if self.currentPosition.y < self.radius:
            self.currentPosition.y = self.radius
            self.oldPosition.y = self.currentPosition.y + velocity.y * 0.8
        if self.currentPosition.x > screenWidth - self.radius:
            self.currentPosition.x = screenWidth - self.radius
            self.oldPosition.x = self.currentPosition.x + velocity.x * 0.8
        if self.currentPosition.x < self.radius:
            self.currentPosition.x = self.radius
            self.oldPosition.x = self.currentPosition.x + velocity.x * 0.8

# Function to create particles
def create_particles(color, amount, size):
    particles = []
    for i in range(amount):
        x = random.randint(10, screenWidth - 10)
        y = random.randint(10, screenHeight - 10)
        particles.append(VerletObject(x, y, size, color))
    return particles

# Solver class to handle physics updates
class Solver:
    def __init__(self):
        self.particles = create_particles(MAROON, 15, 15)

    def update(self, dt):
        for obj in self.particles:
            if gravity_enabled:
                obj.apply_acceleration(gravity)
            obj.update(dt)
            obj.draw()

    def handle_collisions(self):
        for i in range(len(self.particles)):
            for j in range(i + 1, len(self.particles)):
                self.check_collision(self.particles[i], self.particles[j])

    def check_collision(self, obj1, obj2):
            collision_axis = obj1.currentPosition - obj2.currentPosition
            distance = collision_axis.length()
            min_distance = obj1.radius + obj2.radius

            if distance < min_distance:
                overlap = min_distance - distance
                normal = collision_axis.normalize()

                # Move the objects apart based on their masses
                obj1.currentPosition += normal * (overlap * obj2.mass / (obj1.mass + obj2.mass))
                obj2.currentPosition -= normal * (overlap * obj1.mass / (obj1.mass + obj2.mass))

                # Calculate relative velocity
                relative_velocity = obj1.currentPosition - obj1.oldPosition - (obj2.currentPosition - obj2.oldPosition)

                # Calculate the velocity along the normal
                velocity_along_normal = relative_velocity.dot(normal)

                # Apply collision impulse if they are moving towards each other
                if velocity_along_normal < 0:
                    restitution = 0.9  # Elasticity of the collision
                    impulse_strength = -(1 + restitution) * velocity_along_normal / (1 / obj1.mass + 1 / obj2.mass)
                    impulse = normal * impulse_strength

                    obj1.oldPosition -= impulse * (1 / obj1.mass)
                    obj2.oldPosition += impulse * (1 / obj2.mass)


    def add_particle(self, x, y, size, color):
        self.particles.append(VerletObject(x, y, size, color))

    def reset(self):
        self.particles.clear()

def draw_button(text, rect):
    pygame.draw.rect(screen, BLACK, rect)
    font = pygame.font.SysFont(None, 24)
    text_surf = font.render(text, True, WHITE)
    screen.blit(text_surf, (rect.x + (rect.width - text_surf.get_width()) // 2, rect.y + (rect.height - text_surf.get_height()) // 2))

def main():
    clock = pygame.time.Clock()
    solver = Solver()

    running = True
    while running:
        dt = clock.tick(60) / 1000  # Delta time in seconds

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if add_button_rect.collidepoint(event.pos):
                    solver.add_particle(random.randint(10, screenWidth - 10), random.randint(10, screenHeight - 10), 15, MAROON)
                elif reset_button_rect.collidepoint(event.pos):
                    solver.reset()
                elif toggle_gravity_rect.collidepoint(event.pos):
                    global gravity_enabled
                    gravity_enabled = not gravity_enabled

        # Update simulation
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, (0, floor_height, screenWidth, 5))  # Floor line

        solver.update(dt)
        solver.handle_collisions()

        # Draw buttons
        draw_button("Add Ball", add_button_rect)
        draw_button("Reset", reset_button_rect)
        draw_button("Toggle Gravity", toggle_gravity_rect)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
