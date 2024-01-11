import pygame
import math
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
CYAN = [50, 178, 235]
ORANGY = (255, 165, 115)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

ratio = 4 / 5
max_r = 150
wid = 1
gravity = 0
piss_strength = 15
retention_factor = 1.01
press = False
limited = True
particles = []
center = (WIDTH / 2, HEIGHT / 2)
center_v = [WIDTH / 2, HEIGHT / 2]

def update_color(color, color_v):
    for i in range(3):
        color[i] += color_v[i]

        if color[i] <= 3:
            color[i] = 4
            color_v[i] *= -1

        if color[i] >= 253:
            color[i] = 252
            color_v[i] *= -1

def overlap_vector(particle):
    angle = math.atan2(particle[0][1] - center_v[1], particle[0][0] - center_v[0])
  
    
    radi_pos = [center_v[0] + max_r * math.cos(angle),
                center_v[1] + max_r * math.sin(angle)]
    
    offset_v = [particle[0][0] - radi_pos[0], particle[0][1] - radi_pos[1]]

    return offset_v






def particleS():
    global CYAN  # Add this line to make CYAN global

    Pspawn = list(center)
    m_pos = pygame.mouse.get_pos()
    x_r = m_pos[0] - Pspawn[0]
    y_r = m_pos[1] - Pspawn[1]
    theta = math.atan2(y_r, x_r)
    
    color = list(CYAN)  # Create a new copy for each particle
    color_v = [5, -5, 0]
    update_color(color, color_v)

    if press:
        particles.append([Pspawn,
                          [piss_strength * math.cos(theta), piss_strength * math.sin(theta)],
                            random.randint(3, 7),
                          color])
        
        

    for particle in particles:



        if press:
            particle[2] -= 0.1 

        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[1][1] += gravity 
        
        update_color(particle[3], color_v)  # Update the color of each particle
        pygame.draw.circle(screen, particle[3], [(particle[0][0]), (particle[0][1])], particle[2])


        r_x = particle[0][0] - center_v[0]
        r_y = particle[0][1] - center_v[1]
        r = math.sqrt((r_x)**2 + (r_y)**2)
        angle = math.atan2(r_y, r_x)
        r_v = [r_x, r_y]

        overlap = r + particle[2] - max_r
        
        if particle[2] <= 0.5:
            particles.remove(particle)
        
        
        
        if limited:
            if r >= max_r - particle[2]:
                particle[1][1] *= - retention_factor
                particle[1][0] *= - retention_factor 
        else:
            if r > max_r + 2*particle[2]:
                particle[1][0] *= 0.9
                particle[1][1] *= 0.9
            
        


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                press = True
            
            # Clear the balls from list
            if event.key == pygame.K_c:
                particles.clear()
            
            if event.key == pygame.K_0:
                limited = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                press = False 

            if event.key == pygame.K_0:
                limited = False 

    screen.fill((0, 0, 0))
    particleS()
    #pygame.draw.circle(screen, WHITE, center, max_r + wid, wid)
    

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
