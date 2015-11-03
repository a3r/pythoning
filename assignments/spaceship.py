# program template for Spaceship
import simplegui
import math
import random

# globals for user interface

ASSETS_PATH = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
WIDTH = 800
HEIGHT = 600

score = 0
lives = 3
time = 0
inputs = {"left" : -.1, "right": .1}
started = False


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image(ASSETS_PATH + "lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image(ASSETS_PATH + "lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image(ASSETS_PATH + "lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image(ASSETS_PATH + "lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image(ASSETS_PATH + "lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image(ASSETS_PATH + "lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image(ASSETS_PATH + "lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound(ASSETS_PATH + "sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound(ASSETS_PATH + "sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound(ASSETS_PATH + "sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound(ASSETS_PATH + "sounddogs/explosion.mp3")


class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        if self.lifespan:
            self.age += 1
            if self.age > self.lifespan:
                return True
            
        self.fix_position()

    def fix_position(self):
        if self.pos[0] <= 0:
            self.pos[0] = WIDTH
        elif self.pos[0] >= WIDTH:
            self.pos[0] = 0
        if self.pos[1] <= 0: 
            self.pos[1] = HEIGHT
        elif self.pos[1] >= HEIGHT:
            self.pos[1] = 0
            
    def collide(self, other):
        p = self.pos
        q = other.pos
        r1 = self.radius
        r2 = other.radius
        
        distance = dist(p,q)
        if distance <= r1 + r2:
            return True
        else:
            return False
    

def group_collide(set_group, other_object):
    for element in set(set_group):
        if other_object.collide(element):
            set_group.remove(element)
            return True
            
    else:
        return False

def group_group_collide(group1, group2):
    global score
    n = 0
    for element in set(group1):
        if group_collide(group2, element):
            n += 1 
            group1.discard(element)
    return n

class Ship(Sprite):
    def __init__(self, pos, vel, angle, angle_vel, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def rotate(self, acceleration):
        self.angle_vel += acceleration
    
    def update(self):
        friction = 0.015
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vel[0] *= (1-friction)
        self.vel[1] *= (1-friction)
        
        if self.thrust:
            forward = angle_to_vector(self.angle)
            self.vel[0] += forward[0] * 0.2
            self.vel[1] += forward[1] * 0.2
        
        self.fix_position()
       
    def shoot(self):
        
        global missile_group
        
        forward = angle_to_vector(self.angle)
        position = [my_ship.pos[0] + my_ship.radius * forward[0], 
                    my_ship.pos[1] + my_ship.radius * forward[1]]
        
        velocity = [my_ship.vel[0] + forward[0] * 3, 
                    my_ship.vel[1] + forward[1] * 3]
        
        a_missile = Sprite(position, velocity, 0, 0,
                           missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        missile_sound.rewind()
        missile_sound.play()

    def start_thrust(self):
        self.thrust = True
        self.image_center[0] += self.image_size[0]
        ship_thrust_sound.rewind()
        ship_thrust_sound.play()

    def stop_thrust(self):
        self.thrust = False
        self.image_center[0] -= self.image_size[0]
        ship_thrust_sound.pause()

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def click(pos):
    global started, score, lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
    lives = 3
    score = 0
    soundtrack.rewind()
    soundtrack.play()
    
def process_sprite_group(group, canvas):
    global lives
    rm = set([])
    for element in group:
        element.draw(canvas)
        element.update()
        if element.update():
            rm.add(element)
    group.difference_update(rm)
    
def draw(canvas):
    global time, lives, score, started, rock_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("Lives: " + str(lives), (WIDTH - 150, 50), 30, "White")
    canvas.draw_text("Score: " + str(score), (WIDTH - 150, 80), 30, "White")

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    my_ship.update()
    
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

    if group_collide(rock_group, my_ship):
        lives -= 1
    
    score += group_group_collide(missile_group, rock_group)
    
    if lives == 0:
        started = False 
        rock_group = set([])
        soundtrack.pause()
        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, score
    
    if not started:
        return
    
    if len(rock_group) > 12:
        return
    
    pos = None
    while not pos or dist(pos, my_ship.pos) < 5 * my_ship.radius:
        pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
    
    vel = [random.randrange(-1, 2) * (float(score) / 10), random.randrange(-1, 2) * (float(score) / 10)]
    angle_vel = random.randrange(-2, 3) * 0.05
    a_rock = Sprite(pos, vel, 0, angle_vel, asteroid_image, asteroid_info)
    rock_group.add(Sprite(a_rock.pos, a_rock.vel, 0, a_rock.angle_vel, asteroid_image, asteroid_info))
       
        
def keydown(key):
    global acceleration

    for i in inputs:
        if key == simplegui.KEY_MAP[i]:
            acceleration = inputs[i]
            my_ship.rotate(acceleration)
    if key == simplegui.KEY_MAP["up"]:
        my_ship.start_thrust()
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
                
def keyup(key):
    global acceleration
    
    for i in inputs:
        if key == simplegui.KEY_MAP[i]:
            acceleration = -inputs[i]
            my_ship.rotate(acceleration)
    if key == simplegui.KEY_MAP["up"]:
        my_ship.stop_thrust()
        
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0.0, 0.0], 0, 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])


# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()


