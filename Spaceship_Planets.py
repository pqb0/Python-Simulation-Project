import math
import random

import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (50, 178, 235)
LGREY = (211, 211, 211)
DGREY = (58, 59, 60)
ORANGY = (255, 165, 115)
BORANGE = (104, 35, 0)

#Camara Scroll Vectors
scroll = [0,0]
scroll_v = [0,0]
scroll_rate = 5
release_x = False
release_y = False

# Variables 
G = 0.05

bounce_stop = 0.7
Fueling = False
grounded = False
RTurn = False
LTurn = False
tilt_f = 0.01

particles = []

# Initialize pygame
pygame.init()
screen_size = (900, 600)
  
# create a window
screen = pygame.display.set_mode(screen_size)
screen_rect = screen.get_rect()
pygame.display.set_caption("Solar System")

# World Functions

def orbit_v(star_mass, r_init, G):
    return math.sqrt(G * star_mass /r_init)

def CancelJump(ship, c, sun):
    
    if abs(ship.v[c]) > bounce_stop:
                ship.v[c] = (-0.3) * ship.v[c]
    else:
        

        if abs(ship.v[c]) <= bounce_stop:
            if not Fueling:
                ship.v = sun.v
                scroll_v = sun.v
                
            else:
                ship.v[c] += ship.a_vector[c]
            
def Thrust(ship):

    if ship.fuel >= 0:
        if not Fueling:
            return 0
        else:
            ship.fuel -= 0.05
            return -15
    else:
        return 0 


class Planet:
    def __init__(self, mass, radius, sx, sy, vx, vy, color, Fx = 0, Fy = 0,):
        self.mass = mass
        self.radius = radius
        self.pos = [sx, sy]
        self.v =[vx, vy]
        self.color = color
        self.orbital_r = 0


    def drawP(self, sun):
        self.circle = [self.pos[0] - scroll[0], self.pos[1] - scroll[1]]

        pygame.draw.circle(screen, self.color, self.circle , self.radius)
        
    
    def updatePos(self):

        self.pos[0] += self.v[0]
        self.pos[1] += self.v[1]
    
    def OrbitV_update(self, sun):
        r_init = math.sqrt((sun.pos[0] - self.pos[0])**2 + (sun.pos[1] - self.pos[1])**2)

        Vx_orbit = orbit_v(sun.mass, r_init, G) * (self.pos[1] - sun.pos[1]) / r_init
        Vy_orbit = orbit_v(sun.mass, r_init, G) * (sun.pos[0] - self.pos[0]) / r_init

        self.v = [Vx_orbit, Vy_orbit]
        self.orbital_r = r_init
    
    def UpdateGrav(self, sun):
        # Variables for gravitational field force due to Sun
        T = math.atan2((sun.pos[1] - self.pos[1]),(sun.pos[0] - self.pos[0]))
        r = math.sqrt((sun.pos[0] - self.pos[0])**2 + (sun.pos[1] - self.pos[1])**2)
        r = max(r, sun.radius + self.radius)

        # Gravitational field equation
        F = G * self.mass * sun.mass / (r**2)
        self.Fx = F * math.cos(T)
        self.Fy = F * math.sin(T)
                
        # Updating Force and Velocity due to acceleration
        self.v[0] += self.Fx / self.mass 
        self.v[1] += self.Fy / self.mass 
       
# Planets
earth = Planet(300, 355, 2000, screen_size[1]/2, 0,0, CYAN)
mars = Planet(400, 575, 2800, screen_size[1]/2, 0,0, BORANGE)
planets = [earth, mars]


# Sun Class
class Sun():


    def __init__(self, x, y, radius, mass):     # init function for class
       
        self.pos = [x, y]
        self.v = [0, 0]
        self.radius = radius
        self.mass = mass
    
    def drawStar(self, ship):     # star draw function
        self.circle = [self.pos[0] - scroll[0], self.pos[1] - scroll[1]]
        
        pygame.draw.circle(screen, ORANGY, self.circle, self.radius)

        pygame.draw.aaline(screen, 'red', ship.pos, self.circle)

sun = Sun(screen_size[0]/2, 3*screen_size[1] + 500, 1750, 500000)

gravitons = [sun, earth, mars]

# Ship Class
class Ship():
    def __init__(self, x_pos, y_pos, vx, vy, width):
        self.pos = [x_pos, y_pos]
        self.v = [vx, vy]
        self.fuel = 100
        self.mass = width* 10
        self.dimensions = [width, 2 * width]
        self.Tilt = 0
        self.angle = 0
        self.ship_image = pygame.image.load("/Users/pabo/Desktop/PythonFolder1/Repo/Python-Simulation-Project/images/spaceship.png")
 
    def UpdatePos(self):
        scroll[0] += self.v[0]
        scroll[1] += self.v[1]
    
    def Force(self, star1, gravitons):
        global ratio, grounded, G, scroll

        # Thrust Force
        F_t = Thrust(self)
        F_tx = F_t * math.sin(self.angle)
        F_ty = F_t * math.cos(self.angle)
        a_thrust = [F_tx / self.mass, F_ty / self.mass]

        for sun in gravitons:

            dx = sun.circle[0] - self.pos[0]
            dy = sun.circle[1] - self.pos[1]
            r = math.sqrt(dx**2 + dy**2)
            
            min_r = sun.radius + self.dimensions[0]

            T = math.atan2(dy, (sun.circle[0] - self.pos[0]))
            r = max(r, sun.radius)
            r_v = [r * math.cos(T), r * math.sin(T)]

            # Gravitational field equation
            F_w = G * self.mass * sun.mass / (r**2)

            # Net Force
            F_net = F_w
            # Acceleration
            a_net = F_net / self.mass
            self.a_vector = [a_net * math.cos(T) - a_thrust[0], a_net * math.sin(T) + a_thrust[1]]

            if F_w <= 10:
                F_w = 10

            self.v[0] += self.a_vector[0]

            if r >= min_r:
                self.v[1] += self.a_vector[1]
                self.v[0] *= 1
                self.v[1] *= 1

                

                grounded = False

                if RTurn == True:
                    self.angle += tilt_f
                if LTurn == True:
                    self.angle -= tilt_f
            else:
                grounded = True


            overlap = sun.radius + self.dimensions[0] - r

            

            if r < min_r:
                # Calculate the normal vector pointing away from the planet's center
                normal = [self.pos[0] - sun.pos[0], self.pos[1] - sun.pos[1]]
                normal_length = math.sqrt(normal[0]**2 + normal[1]**2)
                normal = [normal[0] / normal_length, normal[1] / normal_length]

                # Move the ship just outside the sun's surface
                overlap = min_r - r
                self.pos[0] += normal[0] * overlap
                self.pos[1] += normal[1] * overlap

                # Stop the ship's motion when it lands
                self.v = [0, 0]

                
                

            if grounded == True:
                self.angle = T - math.pi/2
                CancelJump(self, 0, sun)
                CancelJump(self, 1, sun)

                if self.fuel < 100:
                    self.fuel += 0.5
                else:
                    self.fuel = 100
            
            # Draw acceleration arrow (black)
        acc_arrow_length = 200
        acc_arrow_color = BLACK
        acc_arrow_end = [self.pos[0] + acc_arrow_length * self.a_vector[0], 
                         self.pos[1] + acc_arrow_length * self.a_vector[1]]
        pygame.draw.line(screen, acc_arrow_color, self.pos, acc_arrow_end, 2)
    

    def drawUpdate(self, sun):
        scaled_ship = pygame.transform.scale(self.ship_image, (1.3 * self.dimensions[1], self.dimensions[1]))
        rotated_ship = pygame.transform.rotate(scaled_ship, math.degrees(-self.angle))
        ship_rect = rotated_ship.get_rect(center=(self.pos[0], self.pos[1]))
        screen.blit(rotated_ship, ship_rect)


        global particles

        # Draw fuel bar
        fuel_bar_width = 100
        fuel_bar_height = 10
        fuel_bar_color = (0, 255, 0)  # Green color for fuel
        fuel_level = max(0, self.fuel) / 100  # Normalize fuel level to [0, 1]
        fuel_bar_rect = pygame.Rect(self.pos[0] - fuel_bar_width / 2, self.pos[1] - self.dimensions[0] - 20,
                                    fuel_bar_width * fuel_level, fuel_bar_height)
        pygame.draw.rect(screen, fuel_bar_color, fuel_bar_rect)

        midbottomx, midbottomy = ship_rect.midbottom
        Pspawn = [midbottomx - self.dimensions[0] * math.sin(self.angle),
                  ship_rect.centery + self.dimensions[0] * math.cos(self.angle)]

                
        if Fueling == True and self.fuel > 0:
            color_options = [BORANGE, DGREY, BLACK]
            particles.append([Pspawn,
                              [random.randint(-20, 50)/10 - 1, 2],
                              random.randint(int(self.dimensions[0] / 6), int(self.dimensions[0] / 5)),
                              random.choice(color_options)])

        for particle in particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            pygame.draw.circle(screen, particle[3], [int(particle[0][0]), int(particle[0][1])], particle[2])

    
            if particle[2] <= 0:
                particles.remove(particle)

        

spaceship = Ship(screen_size[0]/2, screen_size[1]/2, 0,0, 20)
  

# Clock for controlling the frame rate
clock = pygame.time.Clock()


running = True
while running:

    screen.fill((2, 50, 120))
    sun.drawStar(spaceship)

    for planet in planets:
        planet.drawP(sun)
        planet.UpdateGrav(sun)
        planet.updatePos()
        planet.OrbitV_update(sun)

     # ship
 
    spaceship.drawUpdate(sun)
    spaceship.UpdatePos()
    spaceship.Force(sun, gravitons)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:    
            # Fueling Start
            if event.key == pygame.K_SPACE:
                Fueling = True
            if event.key == pygame.K_d:
                RTurn = True
            if event.key == pygame.K_a:
                LTurn = True
             

        
        if event.type == pygame.KEYUP:    
            # Fueling End
            if event.key == pygame.K_SPACE:
                Fueling = False   
            if event.key == pygame.K_d:
                RTurn = False
            if event.key == pygame.K_a:
                LTurn = False     
           
       
  


    # Cap the frame rate
    clock.tick(60)

    # Update the display
    pygame.display.flip()