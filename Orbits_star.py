import pygame, math, random

# Boilerplate
WIDTH = 1200
HEIGHT = 700
screen = pygame.display.set_mode([WIDTH, HEIGHT]) 
run = True
fps = 60
timer = pygame.time.Clock()

# variables
wall_thickness = 30
bounce_stop = 0.4
G = 50

#Camara 
scroll = [0,0]
scroll_v = [0,0]
release_x = False
release_y = False

zoom_in = False
zoom_out = False


multiplier = 1.1  # Adjust this value to control the zoom speed
max_zoom = 5.0
scaling_factor = 1

# Walls
def drawBoundaries():
    pygame.draw.line(screen, 'white', [0, HEIGHT], [WIDTH, HEIGHT], wall_thickness)
    pygame.draw.line(screen, 'white', [0, 0], [0, HEIGHT], wall_thickness)
    pygame.draw.line(screen, 'white', [0, 0], [WIDTH, 0], wall_thickness)
    pygame.draw.line(screen, 'white', [WIDTH, 0], [WIDTH, HEIGHT], wall_thickness)

def orbit_v(star_mass, r_init, G):
    return math.sqrt(G * star_mass / r_init)

def zoom(obj, multiplier=1.1, min_radius=5, max_radius=500):
    global scaling_factor  # Assuming this variable is declared globally

    o_posx = obj.p[0]
    o_posy = obj.p[1]

    # Calculate the new radius based on zoom
    if zoom_in:
        obj.radius *= multiplier
        obj.p[0] *= multiplier
        obj.p[1] *= multiplier
        scaling_factor *= multiplier
      
    if zoom_out:
        obj.radius /= multiplier 
        obj.p[0] /= multiplier
        obj.p[1] /= multiplier
        scaling_factor /= multiplier

    # Ensure the radius is within the specified bounds
    obj.radius = max(min(obj.radius, max_radius), min_radius)

# ball class
class Ball():
    def __init__(self, x_pos, y_pos, radius, mass, vx, vy, retention, Fx = 0, Fy = 0):
        self.p = [x_pos, y_pos]
        self.Dp = [x_pos, y_pos]
        self.radius = radius
        self.mass = mass
        self.v = [vx, vy]
        self.retention = retention
        self.circle = ''
        self.selected = False

    # position function
    def UPos(self, mouse_coords):  
       
        # condition for mouse press in position
        if not self.selected:
            self.p[0] += self.v[0]
            self.p[1] += self.v[1]
        else:
            [self.p[0], self.p[1]] = mouse_coords
            vy = 0
    
    # force function
    def UResultantForce(self, star1):
        # Variables for gravitational field force due to star 1
        T = math.atan2((star1.Dp[1] - self.p[1]),(star1.Dp[0] - self.p[0]))
        r = math.sqrt((star1.Dp[0] - self.p[0])**2 + (star1.Dp[1] - self.p[1])**2)
        r = max(r, star1.radius + self.radius)
            
        # Condition for mouse selection
      

        if not self.selected:
            # Gravitational field equation
            F_star = G * self.mass * star1.mass / (r**2)
            F_sx = F_star * math.cos(T)
            F_sy = F_star * math.sin(T)
                

                # Updating Force and Velocity due to acceleration
            self.v[0] += F_sx / self.mass 
            self.v[1] += F_sy / self.mass 
        else:
            self.v[0] = 0
            self.v[1] = 0

    def check_select(self, mouse_coords):       # function checks if mouse_pos with ball collision exists
        self.selected = False
        if self.circle.collidepoint(mouse_coords):
            self.selected = True
        
    
    def drawB(self):     # ball draw function
        self.circle = pygame.draw.circle(screen, 'white', (self.p[0] + scroll[0], self.p[1] + scroll[1]), self.radius)

# Star class
class Star():
    def __init__(self, x, y, radius, mass):     # init function for class
       
        self.p = [x, y]
        self.radius = radius 
        self.mass = mass
        self.Dp = [x, y]
    
    def draw(self):     # star draw function
        self.circle = pygame.draw.circle(screen, 'black', (self.Dp[0] + scroll[0], self.Dp[1] + scroll[1]), self.radius)




# ball instances
ball1 = Ball(700, 400, 20, 20, 0, 0, 0, 0, 0)
ball2 = Ball(300, 400, 30, 20, 0, 0, 0, 0, 0)

balls = [ball1]


# ball list


# star instances
star1 = Star(WIDTH/2, HEIGHT/2 , 50, 50)
# star list
stars = [star1]


# Main Game Loop
while run:
    timer.tick(fps)
    screen.fill((0,10,80))

    mc = list(pygame.mouse.get_pos())
    mouse_coords = [mc[0] - scroll[0], mc[1] - scroll[1]]

    #scroll update for camera
    scroll[0] += scroll_v[0]
    scroll[1] += scroll_v[1]
    if abs(scroll_v[0]) <= 0.05:
        scroll_v[0] = 0
    if abs(scroll_v[1]) <= 0.05:
        scroll_v[1] = 0

    #camara drift
    if release_x == True:
        scroll_v[0] *= 0.95
    
    if release_y == True:
        scroll_v[1] *= 0.95


    for ball in balls:      # loop for all ball functions in balls
        ball.drawB()
        ball.UPos(mouse_coords)
        ball.UResultantForce(star1)
        zoom(ball)

    star1.draw()
    zoom(star1)
    drawBoundaries()
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:       # Mouse button down position with ball check
            if event.button == 1:
                for ball in balls:
                    if ball.check_select(event.pos):
                        select = True

        if event.type == pygame.MOUSEBUTTONUP:    # Mouse button up check
            if event.button == 1:
                select = False
                for i in range(len(balls)):
                    balls[i].check_select((-10000,-10))

        if event.type == pygame.KEYDOWN:
            # Use SPACE00 to create new balls
            if event.key == pygame.K_SPACE:
                r_init = math.sqrt((star1.Dp[0] - mouse_coords[0])**2 + (star1.Dp[1] - mouse_coords[1])**2)
                Vx_orbit = orbit_v(star1.mass, r_init, G) * (mouse_coords[1] - star1.Dp[1]) / r_init
                Vy_orbit = orbit_v(star1.mass, r_init, G) * (star1.Dp[0] - mouse_coords[0]) / r_init

                
                balls.append(Ball(mouse_coords[0], mouse_coords[1], scaling_factor*random.randint(10, 35), 
                            random.randint(10, 40), Vx_orbit, Vy_orbit, 1, 0))

                #Camara scroll keystrokes
            if event.key == pygame.K_d:
                release_x = False
                scroll_v[0] = -3
            if event.key == pygame.K_a:
                release_x = False
                scroll_v[0] = 3
            if event.key == pygame.K_w:
                release_y = False
                scroll_v[1] = 3
            if event.key == pygame.K_s:
                release_y = False
                scroll_v[1] = -3

            # Use K_0 to stop force due to star1
            if event.key == pygame.K_0:
                star1.mass = 0
            
            # SUck stars
            if event.key == pygame.K_g:
                G = 999

            # Clear the balls from list
            if event.key == pygame.K_c:
                balls.clear()


            # Camera Scaling zoom in
            if event.key == pygame.K_UP:
                zoom_in = True
            # Camera Scaling zoom out
            if event.key == pygame.K_DOWN:
                zoom_out = True


            for ball in balls:
                if ball.selected == True:
                    if event.key == pygame.K_t:
                        ball.radius = 1.4*ball.radius
                        ball.mass = ball.radius
                    
                    if event.key == pygame.K_y:
                        ball.radius = (3/5)*ball.radius
                        ball.mass = ball.radius
                    
                    
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_g:
                G = 50
            # Use K_0 to star force due to star1
            if event.key == pygame.K_0:
                star1.mass = 50
            
            if event.key == pygame.K_d or event.key == pygame.K_a:
                release_x = True
             
            if event.key == pygame.K_w or event.key == pygame.K_s:
                release_y = True
            

            # Camera Scaling zoom in
            if event.key == pygame.K_UP:
                zoom_in = False
                    

            # Camera Scaling zoom out
            if event.key == pygame.K_DOWN:
                zoom_out = False

        if event.type == pygame.QUIT:
            run = False
    
       
    pygame.display.update()
    pygame.display.flip()

pygame.quit()


