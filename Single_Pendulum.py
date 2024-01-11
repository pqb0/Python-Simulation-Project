import pygame
import math

# Initialize Pygame
pygame.init()

# Set up display dimensions and scaling factor
scale = 2
width, height = 800, 600
screen = pygame.display.set_mode((width * scale, height * scale))

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CYAN = (0, 183, 235)

# Set up the clock
clock = pygame.time.Clock()

gravity = 1.2  # Acceleration due to gravity

# Pendulum parameters
class Pendulum:
    def __init__(self, origin_x, origin_y, length, weight, angle, angular_v, damping):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.length = length
        self.weight = 20
        self.angle = math.pi / 4 
        self.angular_v = angular_v 
        self.damping = damping  
        self.trace = []
        self.timer = 0
        self.selected = False
        self.mass = ''


    

    def update(self, delta_time):
        global ball_x
        global ball_y
        ball_x = self.origin_x + self.length * math.sin(self.angle)
        ball_y = self.origin_y + self.length * math.cos(self.angle)

        if not self.selected:
            angular_acceleration = (-gravity / self.length) * math.sin(self.angle)
            self.angular_v += angular_acceleration
            self.angular_v *= self.damping
            self.angle += self.angular_v
        else:
             self.angular_v = 0
             angle_to_mouse = math.atan2(mouse_coords[1] - self.origin_y, mouse_coords[0] - self.origin_x)
             self.angle = math.pi/2 - angle_to_mouse 

        

       
    
    def draw(self):
        # Store the position of the ball for trace
        ball_x = self.origin_x + self.length * math.sin(self.angle)
        ball_y = self.origin_y + self.length * math.cos(self.angle)
        self.trace.append((ball_x, ball_y))
        self.timer += delta_time

        for point in self.trace:
            pygame.draw.circle(screen, CYAN, (int(point[0]), int(point[1])), 1)

            if self.timer > 16:
                self.trace.remove(point)
                self.timer = 0
    
        # Draw the rod
        pygame.draw.aaline(screen, BLACK, (self.origin_x, self.origin_y), (ball_x, ball_y), 2)
        # Draw the weight
        self.circle = pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), self.weight)
    
    def check_select(self, mouse_coords):       # function checks if mouse_pos with ball collision exists
        self.selected = False
        if self.circle.collidepoint(mouse_coords):
            self.selected = True
    

pend1 = Pendulum(width // 2, 100, 200, 20, math.pi / 4, 0, 0.995)

Penduli = [pend1]

# Main loop
running = True
while running:
    delta_time = clock.tick(60)

    mouse_coords = pygame.mouse.get_pos()

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:       # Mouse button down position with ball check
            if event.button == 1:
                for pend in Penduli:
                    if pend1.check_select(event.pos):
                        select = True

        if event.type == pygame.MOUSEBUTTONUP:    # Mouse button up check
            if event.button == 1:
                select = False
                for i in range(len(Penduli)):
                    Penduli[i].check_select((-10000,-10))

    screen.fill(WHITE)

  
    pend1.draw()
    pend1.update(delta_time)

    # Scale the screen to the desired size
    scaled_screen = pygame.transform.scale(screen, (width * scale, height * scale))
    pygame.display.set_caption("Pendulum Simulation")
    pygame.display.flip()

pygame.quit()
