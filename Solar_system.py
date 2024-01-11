import pygame
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DORANGY = (100, 29, 30)
CYAN = (50, 178, 235)
ORANGY = (255, 165, 115)
YEL = (214, 170, 40)
LBROWN = (195, 155, 119)
LGREY = (211, 211, 211)

# initialize pygame
pygame.init()
screen_size = (900, 600)

# create a window
screen = pygame.display.set_mode(screen_size)
screen_rect = screen.get_rect()
pygame.display.set_caption("Solar System")

# Variables
G = 10
scroll_rate = 5
# Camara Scroll Vectors
scroll = [0, 0]
scroll_v = [0, 0]
release_x = False
release_y = False


def CameraUpdate():
    scroll[0] += scroll_v[0]
    scroll[1] += scroll_v[1]
    if abs(scroll_v[0]) <= 0.05:
        scroll_v[0] = 0
    if abs(scroll_v[1]) <= 0.05:
        scroll_v[1] = 0

    # camera drift
    if release_x:
        scroll_v[0] *= 0.95

    if release_y:
        scroll_v[1] *= 0.95


# Orbit Velocity Function
def orbit_v(star_mass, r_init, G):
    return math.sqrt(G * star_mass / r_init)


# Sun Class
class Sun():
    def __init__(self, x, y, radius, mass):  # init function for class

        self.s = [x, y]
        self.radius = radius
        self.mass = mass

    def drawStar(self):  # star draw function
        self.circle = pygame.draw.circle(screen, ORANGY, (self.s[0] + scroll[0], self.s[1] + scroll[1]),
                                         self.radius)


sun = Sun(screen_size[0] / 2, screen_size[1] / 2, 150, 50)

# Planet Class
class Planet:
    def __init__(self, mass, radius, sx, sy, vx, vy, color, Fx=0, Fy=0):
        self.mass = mass
        self.radius = radius
        self.pos = [sx, sy]
        self.v = [vx, vy]
        self.color = color
        self.orbital_r = 0

    def drawP(self, sun):
        pygame.draw.circle(screen, WHITE, [sun.s[0] + scroll[0], sun.s[1] + scroll[1]], self.orbital_r, 1)
        pygame.draw.circle(screen, self.color, [self.pos[0] + scroll[0], self.pos[1] + scroll[1]], self.radius)

    def updatePos(self):
        self.pos[0] += self.v[0]
        self.pos[1] += self.v[1]

    def OrbitV_update(self, sun):
        r_init = math.sqrt((sun.s[0] - self.pos[0]) ** 2 + (sun.s[1] - self.pos[1]) ** 2)
        Vx_orbit = orbit_v(sun.mass, r_init, G) * (self.pos[1] - sun.s[1]) / r_init
        Vy_orbit = orbit_v(sun.mass, r_init, G) * (sun.s[0] - self.pos[0]) / r_init

        self.v = [Vx_orbit, Vy_orbit]
        self.orbital_r = r_init

    def UpdateGrav(self, sun):
        # Variables for gravitational field force due to Sun
        T = math.atan2((sun.s[1] - self.pos[1]), (sun.s[0] - self.pos[0]))
        r = math.sqrt((sun.s[0] - self.pos[0]) ** 2 + (sun.s[1] - self.pos[1]) ** 2)
        r = max(r, sun.radius + self.radius)

        # Gravitational field equation
        F = G * self.mass * sun.mass / (r ** 2)
        self.Fx = F * math.cos(T)
        self.Fy = F * math.sin(T)

        # Updating Force and Velocity due to acceleration
        self.v[0] += self.Fx / self.mass
        self.v[1] += self.Fy / self.mass


# Planets
mercury = Planet(50, 15, 800, screen_size[1] / 2, 0, 0, RED)
venus = Planet(75, 20, 1000, screen_size[1] / 2, 0, 0, YEL)
earth = Planet(100, 25, 1200, screen_size[1] / 2, 0, 0, CYAN)
mars = Planet(105, 28, 1400, screen_size[1] / 2, 0, 0, DORANGY)
jupiter = Planet(400, 95, 1800, screen_size[1] / 2, 0, 0, LBROWN)
saturn = Planet(400, 45, 2500, screen_size[1] / 2, 0, 0, LGREY)
uranus = Planet(200, 60, 3500, screen_size[1]/2, 0, 0, LBROWN)
neptune = Planet(180, 55, 4000, screen_size[1]/2, 0, 0, CYAN)

planets = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

# Moon Class
class Moon:
    def __init__(self, mass, radius, mx, my, m_vx, m_vy, color, Fx=0, Fy=0):
        self.mass = mass
        self.radius = radius
        self.ms = [mx, my]
        self.v = [m_vx, m_vy]
        self.color = color
        self.orbital_rm = math.sqrt((earth.pos[0] - self.ms[0]) ** 2 + (earth.pos[1] - self.ms[1]) ** 2)

    def drawP(self, planet):
        pygame.draw.circle(screen, self.color, [self.ms[0] + scroll[0], self.ms[1] + scroll[1]], self.radius)

    def updatePos(self):
        self.ms[0] += self.v[0]
        self.ms[1] += self.v[1]

    def OrbitV_update(self, planet):
        rm_init = math.sqrt((planet.pos[0] - self.ms[0]) ** 2 + (planet.pos[1] - self.ms[1]) ** 2)
        Vx_Morbit = orbit_v(2 * planet.mass, rm_init, G) * (self.ms[1] - planet.pos[1]) / rm_init
        Vy_Morbit = orbit_v(2 * planet.mass, rm_init, G) * (planet.pos[0] - self.ms[0]) / rm_init

        self.v = [Vx_Morbit, Vy_Morbit]

    def UpdateGrav(self, planet):
        # Variables for gravitational field force due to Planet
        T = math.atan2((planet.pos[1] - self.ms[1]), (planet.pos[0] - self.ms[0]))
        r = math.sqrt((planet.pos[0] - self.ms[0]) ** 2 + (planet.pos[1] - self.ms[1]) ** 2)
        r = max(r, planet.radius + self.radius)

        # Gravitational field equation
        F = G * self.mass * planet.mass / (r ** 2)
        self.Fx = F * math.cos(T)
        self.Fy = F * math.sin(T)
        # Updating Force and Velocity due to acceleration
        self.v[0] += self.Fx / self.mass 
        self.v[1] += self.Fy / self.mass


# Lists of Moons for each planet
venus_moons = [Moon(15, 5, venus.pos[0] + 70, venus.pos[1], 0, 0, WHITE)]
earth_moons = [Moon(20, 6, earth.pos[0] + 50, earth.pos[1], 0, -1, LGREY)]

mars_moons = [Moon(10, 4, mars.pos[0] + 50, mars.pos[1] + 30, 0, 0, LBROWN),
              Moon(8, 3, mars.pos[0] + 50, mars.pos[1] - 30, 0, 0, DORANGY)]

jupiter_moons = [Moon(30, 8, jupiter.pos[0] + 160, jupiter.pos[1] + 50, 0, 0, DORANGY),
                 Moon(25, 7, jupiter.pos[0] + 155, jupiter.pos[1] - 50, 0, 0, CYAN),
                 Moon(20, 6, jupiter.pos[0] + 180, jupiter.pos[1], 0, 0, ORANGY),
                 Moon(18, 5, jupiter.pos[0] + 120, jupiter.pos[1], 0, 0, YEL)]

saturn_moons = [Moon(25, 7, saturn.pos[0] + 120, saturn.pos[1] + 40, 0, 0, ORANGY),
                Moon(22, 6, saturn.pos[0] + 120, saturn.pos[1] - 40, 0, 0, YEL),
                Moon(18, 5, saturn.pos[0] + 150, saturn.pos[1] + 30, 0, 0, LGREY),
                Moon(15, 4, saturn.pos[0] + 150, saturn.pos[1] - 30, 0, 0, LBROWN),
                Moon(12, 3, saturn.pos[0] + 180, saturn.pos[1] + 20, 0, 0, RED),
                Moon(10, 2, saturn.pos[0] + 180, saturn.pos[1] - 20, 0, 0, WHITE)]

uranus_moons = [Moon(18, 5, uranus.pos[0] + 100, uranus.pos[1] + 30, 0, 0, DORANGY),
                Moon(16, 4, uranus.pos[0] + 100, uranus.pos[1] - 30, 0, 0, CYAN),
                Moon(14, 4, uranus.pos[0] + 130, uranus.pos[1] + 20, 0, 0, LBROWN),
                Moon(12, 3, uranus.pos[0] + 130, uranus.pos[1] - 20, 0, 0, WHITE)]

neptune_moons = [Moon(22, 6, neptune.pos[0] + 80, neptune.pos[1], 0, 0, ORANGY)]

# Combine all moons into a single list
moons = [venus_moons, earth_moons, mars_moons, jupiter_moons, saturn_moons, uranus_moons, neptune_moons]


# clock is used to set a max fps
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(BLACK)
    CameraUpdate()

    # Update and draw moons for each planet
    for i, planet in enumerate(planets):
        for moon in moons[i - 1]:
            moon.drawP(planet)
            moon.UpdateGrav(planet)
            moon.updatePos()
            moon.OrbitV_update(planet)



    for planet in planets:
        planet.drawP(sun)
        planet.UpdateGrav(sun)
        planet.updatePos()
        planet.OrbitV_update(sun)


    sun.drawStar()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Camera scroll keystrokes
            if event.key == pygame.K_d:
                release_x = False
                scroll_v[0] = -scroll_rate
            if event.key == pygame.K_a:
                release_x = False
                scroll_v[0] = scroll_rate
            if event.key == pygame.K_w:
                release_y = False
                scroll_v[1] = scroll_rate
            if event.key == pygame.K_s:
                release_y = False
                scroll_v[1] = -scroll_rate

        if event.type == pygame.KEYUP:
            # Camera Release check
            if event.key == pygame.K_d or event.key == pygame.K_a:
                release_x = True

            if event.key == pygame.K_w or event.key == pygame.K_s:
                release_y = True

    # how many updates per second
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
