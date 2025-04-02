import pygame
import random 
import math
import time
FPS = 120
FRICTION = 0.70
SCREEN_SIZE = (1000, 800)

ali = 10
coh = 7000
sep = 7000

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector2({"%.2f" % round(self.x, 2)}, {"%.2f" % round(self.y, 2)})"

    def __add__(self, other):

        if type(other) == list or type(other) == tuple:
            return [self.x + other[0], self.y + other[1]]
        return Vector2(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)

    def norm(self):
        return (self.x**2 + self.y**2) ** 0.5  # Compute Euclidean norm

    def normalize(self):
        norm = self.norm()
        if norm != 0:
            self.x /= norm
            self.y /= norm
        return self    

    def negat(self):
        return Vector2(-self.x, -self.y)
        
    def set_length(self, new_length):
        normalized = self.normalize()
        self.x = normalized.x * new_length
        self.y = normalized.y * new_length
        return Vector2(self.x, self.y)
    def to_angle(self):
        return math.atan2(self.y, self.x) * (180 / math.pi)

    def length(self):
        return math.sqrt(self.x **2 + self.y**2)
    
    def get(self):
        return [self.x, self.y]

    def dot(self, other):
        return self.x * other.x + self.y * other.y

class Poly:
    def __init__(self, size):
        self.size = size
        self.wide = 3.5 
    def draw(self, pos,angle, col): #[(pos.y, (-math.sin(angle)* self.size) + pos.x ), (pos.y, (math.sin(angle)* self.size) + pos.x), ( (math.cos(angle)) * self.size + pos.x , (math.sin(angle) * self.size) + pos.y)])
        #pygame.draw.circle(screen, (200, 200, 200), pos.get(), 10)
        pygame.draw.polygon(screen, col, [ ((math.cos(angle)) * self.size + pos.x , (math.sin(angle) * self.size) + pos.y), ((math.cos(angle + math.radians(90)) * (self.size/self.wide) + pos.x , (math.sin(angle + math.radians(90)) * (self.size /self.wide) + pos.y))),  ((math.cos(angle + math.radians(270)) * (self.size/self.wide) + pos.x) , (math.sin(angle + math.radians(270)) * (self.size /self.wide) + pos.y))])

class Color:
    def __init__(self, r=100, g=100, b=100):
        self.r = r
        self.b = b
        self.g = g
    def get(self):
        return (self.r, self.g, self.b)


class Boid:
    def __init__(self, pos, velo, size, dirrection):
        self.pos = pos
        self.velo = velo
        self.size = size
        self.dirrection = math.radians(dirrection)
        self.poly = Poly(size)
        self.flapspeed = .01
        self.maxvel = 1
        self.flapforce = random.randint(1, self.maxvel)
        self.flaptiming = 0
        self.range = 45 
        self.color = Color()
    
    def moy(self, dis):
        somm = 0
        num = 0
        for boid in scene.boids:
            if (self.pos - boid.pos).length() < dis:
                somm += boid.dirrection
                num += 1
        print(somm/num)
        if num == 0:
            num = 1
        return somm / num

    def moypos(self, dist):
        somm = Vector2()
        num = 0
        for boid in scene.boids:
            if (self.pos - boid.pos).length() < dist:
                somm += boid.pos
                num += 1
        return somm / num

    def sommdir(self, dist):
        somm = Vector2()  # Vecteur pour stocker la somme
        for boid in scene.boids:
            if (self.pos - boid.pos).length() < dist and boid != self:
                somm += self.pos - boid.pos  
        if somm.length() > 0:
            return somm.negat().set_length(self.velo).to_angle()
        return 0 


    def move(self):
        self.flaptiming += 1 * dt
        if self.flaptiming >= self.flapspeed:
            self.flaptiming = 0
            self.velo += self.flapforce
            alignement =  (self.moy(self.range) - self.dirrection) / ali
            cohesion = (self.moypos(self.range) - self.pos).to_angle() / coh
            separation = self.sommdir(self.range) / sep
            self.dirrection += alignement + separation + cohesion
            print(self.dirrection)
        self.velo *= FRICTION ** dt
        newpos = self.pos + (Vector2(math.cos(self.dirrection)*self.velo, math.sin(self.dirrection)*self.velo) * dt)
        if newpos.x > SCREEN_SIZE[0] or newpos.x < 0:
            print("aoidhipauzhdpiuad")
            newpos.x = 1 if newpos.x > SCREEN_SIZE[0] else SCREEN_SIZE[0] -1
            
        if newpos.y > SCREEN_SIZE[1] or newpos.y < 0:
            newpos.y = 1 if  newpos.y > SCREEN_SIZE[1] else SCREEN_SIZE[1] -1

        self.pos = newpos  

    def turn(self, deg):
        self.dirrection += math.radians(deg)
    
    def draw(self):
        self.poly.draw(self.pos, self.dirrection, self.color.get())

class Scene:
    def __init__(self):
        self.boids = []
        self.population = len(self.boids)
    def addboid(self, boid):
        self.boids.append(boid)
        self.population += 1
    def upd(self):
        for boid in self.boids:
            boid.move()
            #boid.turn(2)
            boid.draw()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)
Running = True
scene = Scene()

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
    dt = clock.tick(FPS) / 1000 
    if scene.population <= 100 and random.randint(0, 10):

        scene.addboid(Boid(Vector2(random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1])), 100, 20, random.randint(0, 360)))


    screen.fill(0)
    scene.upd()
    pygame.display.flip()



