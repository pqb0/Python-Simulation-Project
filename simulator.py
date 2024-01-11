import pygame
import math
import random 

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Mouse position
mouse_x, mouse_y = 0, 0

#   Conditions
generating = False
removing = False

scaling_factor = 0.9

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Life Simulation")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

def create(c, number, size):
    particles = []
    for i in range(number):
        particles.append([random.randint(10, WIDTH - 10), random.randint(10, HEIGHT - 10), c, [0, 0], size])
    
    return particles
    
def func(p1, p2, g, max_d):
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
        
        a[3][0] +=  fx
        a[3][1] +=  fy

        a[3][0] *=  scaling_factor
        a[3][1] *=  scaling_factor

        a[0] += a[3][0]
        a[1] += a[3][1]

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
        a[3][0] = min( a[3][0], v_max)
        a[3][1] = min( a[3][1], v_max)

red = create('red', 10, 5)
green = create('green', 5, 5)
yellow = create('yellow', 10, 5)
blue = create('blue', 3, 5)
orange = create('orange', 1, 5)
pink = create('pink', 1, 5)
white = create('white', 4, 5)

P_list = [red, blue, green, pink]
colors = ['red', 'blue', 'blue', 'pink']

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

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                generating = False
            
            if event.key == pygame.K_c:
                removing = False

        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos     

    screen.fill((0, 0, 0))

    func(red, red, 0.1, 100)
    func(blue, red, -0.3, 50)
    func(blue, blue, 0.3, 100)
    func(red, green, -0.4, 100)
    func(green, blue, 0.7, 30)
    func (green, red, 0.3, 30)
    func(green, green, -0.3, 60)

    func(pink, blue, -0.8, 35)
    func(pink, pink, -0.2, 250)
    func(pink, green, -0.3, 150)
    func(pink, red, 0.5, 175)


    
    
    for p in P_list:
        if generating:
            radius = 50 # You can adjust this radius
            angle = random.uniform(0, 2 * math.pi)
            offset_x = int(random.randint(0,radius) * math.cos(angle))
            offset_y = int(radius * math.sin(angle))
            p.append([mouse_x + offset_x, mouse_y + offset_y, random.choice(colors), [0, 0], 5]) 

        if removing:
            p.clear()
               
    for p in P_list:
        for i in range(len(p)):
            Prect = (p[i][0], p[i][1], p[i][4], p[i][4])
            pygame.draw.rect(screen, p[i][2], Prect)

    # Update the display
    pygame.display.flip()
    # Cap the frame rate
    clock.tick(60)

pygame.quit()