import pygame
import math
import random 

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Mouse position
mouse_x, mouse_y = 0, 0

# Conditions
generating = False
removing = False
mouse_attraction = False  # Toggle for mouse attraction
scaling_factor = 0.9

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Life Simulation")

# Font for displaying toggles
font = pygame.font.SysFont(None, 24)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

def create(c, number, size):
    particles = []
    for i in range(number):
        particles.append([random.randint(10, WIDTH - 10), random.randint(10, HEIGHT - 10), c, [0, 0], size])
    
    return particles

# Updated func to include attraction to the mouse
def func(p1, p2, g, max_d, mouse_attraction_strength=0.5, mouse_attraction_range=200):
    for i in range(len(p1)):
        fx = 0
        fy = 0
        for j in range(len(p2)):
            a = p1[i]
            b = p2[j]
            dx = a[0] - b[0]
            dy = a[1] - b[1]
            d = math.sqrt(dx**2 + dy**2)
            
            if 0.05 < d < max_d:
                F = g * 1/d
                fx += F * dx * 0.5
                fy += F * dy * 0.5
        
        # Apply mouse attraction force if the toggle is on
        if mouse_attraction:
            dx_mouse = a[0] - mouse_x
            dy_mouse = a[1] - mouse_y
            d_mouse = math.sqrt(dx_mouse**2 + dy_mouse**2)
            
            if d_mouse < mouse_attraction_range:  # Apply attraction if within range
                F_mouse = mouse_attraction_strength * 1 / d_mouse
                fx -= F_mouse * dx_mouse  # Negative sign to pull toward the mouse
                fy -= F_mouse * dy_mouse

        # Update velocities and positions
        a[3][0] += fx
        a[3][1] += fy

        a[3][0] *= scaling_factor
        a[3][1] *= scaling_factor

        a[0] += a[3][0]
        a[1] += a[3][1]

        # Handle wall collisions
        if a[0] >= WIDTH - a[4]:
            a[0] -= 3
            a[3][0] *= (-0.6)
        
        if a[0] <= 0:
            a[0] += 3
            a[3][0] *= (-0.6)

        if a[1] >= HEIGHT - a[4]:
            a[1] -= 3
            a[3][1] *= (-0.6)
        
        if a[1] <= 0:
            a[1] += 3
            a[3][1] *= (-0.6)
   
        v_max = 10
        a[3][0] = min(a[3][0], v_max)
        a[3][1] = min(a[3][1], v_max)

# Create particles
red = create('red', 10, 5)
green = create('green', 5, 5)
yellow = create('yellow', 10, 5)
blue = create('blue', 3, 5)
orange = create('orange', 1, 5)
pink = create('pink', 1, 5)
white = create('white', 4, 5)

P_list = [red, blue, green, pink]
colors = ['red', 'blue', 'green', 'pink']

# Function to display toggle status and buttons
def display_status():
    status_texts = [
        f"Generating: {'ON' if generating else 'OFF'} (Key: Space)",
        f"Removing: {'ON' if removing else 'OFF'} (Key: C)",
        f"Mouse Attraction: {'ON' if mouse_attraction else 'OFF'} (Key: M)"
    ]
    for idx, text in enumerate(status_texts):
        status_surface = font.render(text, True, (255, 255, 255))
        screen.blit(status_surface, (10, 10 + idx * 25))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
       
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                generating = True
            
            if event.key == pygame.K_c:
                removing = True
            
            if event.key == pygame.K_m:  # Toggle mouse attraction with 'M' key
                mouse_attraction = not mouse_attraction

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                generating = False
            
            if event.key == pygame.K_c:
                removing = False

        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos     

    screen.fill((0, 0, 0))

    # Apply particle interactions
    func(red, red, 0.1, 100)
    func(blue, red, -0.3, 50)
    func(blue, blue, 0.3, 100)
    func(red, green, -0.4, 100)
    func(green, blue, 0.7, 30)
    func(green, red, 0.3, 30)
    func(green, green, -0.3, 60)
    func(pink, blue, -0.8, 35)
    func(pink, pink, -0.2, 250)
    func(pink, green, -0.3, 150)
    func(pink, red, 0.5, 175)

    # Apply attraction to mouse if toggled
    for p in P_list:
        func(p, p, 0.1, 100, mouse_attraction_strength=0.3, mouse_attraction_range=200)

    # Handle particle generation and removal
    for p in P_list:
        if generating:
            radius = 50  # You can adjust this radius
            angle = random.uniform(0, 2 * math.pi)
            offset_x = int(random.randint(0, radius) * math.cos(angle))
            offset_y = int(radius * math.sin(angle))
            p.append([mouse_x + offset_x, mouse_y + offset_y, random.choice(colors), [0, 0], 5]) 

        if removing:
            p.clear()
               
    # Draw particles
    for p in P_list:
        for i in range(len(p)):
            Prect = (p[i][0], p[i][1], p[i][4], p[i][4])
            pygame.draw.rect(screen, p[i][2], Prect)

    # Display toggle status and buttons
    display_status()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
