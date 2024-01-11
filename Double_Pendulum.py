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

# Single Pendulum Class
class Pendulum:
    def __init__(self, origin_x, origin_y, length, weight, angle, angular_v, damping):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.length = length
        self.weight = 20
        self.angle = math.pi / 4  # Initial angle in radians
        self.angular_v = angular_v  # Initial angular velocity
        self.damping = damping  # Damping factor for reducing energy over time
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
    


# Double Pendulum Class
class DoublePendulum:
    def __init__(self, origin_x, origin_y, length1, length2, weight1, weight2, angle1, angle2, angular_v1, angular_v2, damping):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.length1 = length1
        self.length2 = length2
        self.weight1 = weight1
        self.weight2 = weight2
        self.angle1 = angle1  # Initial angle in radians
        self.angle2 = angle2  # Initial angle in radians
        self.angular_v1 = angular_v1  # Initial angular velocity
        self.angular_v2 = angular_v2  # Initial angular velocity
        self.damping = damping  # Damping factor for reducing energy over time
        self.trace = []
        self.timer = 0
        self.selected1 = False
        self.selected2 = False

    def update(self, delta_time, pendulum=None):
        global ball1_x, ball1_y, ball2_x, ball2_y
        angular_acceleration1 = (-gravity / self.length1) * math.sin(self.angle1)
        angular_acceleration2 = (-gravity / self.length2) * math.sin(self.angle2)
        angle_to_mouse = math.atan2(mouse_coords[1] - self.origin_y, mouse_coords[0] - self.origin_x)
        if not self.selected2: 
            self.angular_v2 += angular_acceleration2
            self.angular_v2 *= self.damping
            self.angle2 += self.angular_v2
            
        else:
            
            self.angular_v2 = 0
            self.angle2 = math.pi / 2 - angle_to_mouse
        
        if not self.selected1:
            self.angular_v1 += angular_acceleration1
            self.angular_v1 *= self.damping
            self.angle1 += self.angular_v1
        else:
            self.angular_v1 = 0
            self.angle1 = math.pi / 2 - angle_to_mouse



        ball1_x = self.origin_x + self.length1 * math.sin(self.angle1)
        ball1_y = self.origin_y + self.length1 * math.cos(self.angle1)
        ball2_x = ball1_x + self.length2 * math.sin(self.angle2)
        ball2_y = ball1_y + self.length2 * math.cos(self.angle2)

        self.trace.append((int(ball2_x), int(ball2_y)))

    def draw(self):
        for point in self.trace:
            pygame.draw.circle(screen, CYAN, point, 1)

            if self.timer > 16:
                self.trace.remove(point)
                self.timer = 0

        # Draw the rods and weights
        pygame.draw.aaline(screen, BLACK, (self.origin_x, self.origin_y), (ball1_x, ball1_y), 2)
        pygame.draw.aaline(screen, BLACK, (ball1_x, ball1_y), (ball2_x, ball2_y), 2)
        pygame.draw.circle(screen, RED, (int(ball1_x), int(ball1_y)), self.weight1)
        pygame.draw.circle(screen, RED, (int(ball2_x), int(ball2_y)), self.weight2)

    def check_select(self, mouse_coords):  # 
        self.selected = False
        if pygame.Rect(ball2_x - self.weight2, ball2_y - self.weight2, 2 * self.weight2, 2 * self.weight2).collidepoint(mouse_coords):
            self.selected2 = True
        if pygame.Rect(ball1_x - self.weight1, ball1_y - self.weight1, 2 * self.weight1, 2 * self.weight1).collidepoint(mouse_coords):
            self.selected1 = True


double_pendulum = DoublePendulum(600, 100, 200, 150, 20, 20, 0, 0, 0, 0, 1)

# Main loop
running = True
while running:
    delta_time = clock.tick(60)

    mouse_coords = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse button down position with ball check
            if event.button == 1:
                double_pendulum.check_select(event.pos)
                

        if event.type == pygame.MOUSEBUTTONUP:  # Mouse button up check
            if event.button == 1:
                double_pendulum.selected1 = False
                double_pendulum.selected2 = False
                
    screen.fill(WHITE)


    double_pendulum.update(delta_time)
    double_pendulum.draw()

    # Scale the screen to the desired size
    scaled_screen = pygame.transform.scale(screen, (width * scale, height * scale))
    pygame.display.set_caption("Double Pendulum Simulation")
    pygame.display.flip()

pygame.quit()
