import pygame
import random 
import math
import time
FPS = 60
FRICTION = 0.70
SCREEN_SIZE = (1000, 800)

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
    def draw(self, pos,angle): #[(pos.y, (-math.sin(angle)* self.size) + pos.x ), (pos.y, (math.sin(angle)* self.size) + pos.x), ( (math.cos(angle)) * self.size + pos.x , (math.sin(angle) * self.size) + pos.y)])
        #pygame.draw.circle(screen, (200, 200, 200), pos.get(), 10)
        pygame.draw.polygon(screen, (100, 100, 100), [ ((math.cos(angle)) * self.size + pos.x , (math.sin(angle) * self.size) + pos.y), ((math.cos(angle + math.radians(90)) * (self.size/self.wide) + pos.x , (math.sin(angle + math.radians(90)) * (self.size /self.wide) + pos.y))),  ((math.cos(angle + math.radians(270)) * (self.size/self.wide) + pos.x) , (math.sin(angle + math.radians(270)) * (self.size /self.wide) + pos.y))])


class Boid:
    def __init__(self, pos, velo, size, dirrection):
        self.pos = pos
        self.velo = velo
        self.size = size
        self.dirrection = math.radians(dirrection)
        self.poly = Poly(size)
        self.flapspeed = .01
        self.flapforce = 1
        self.flaptiming = 0
    
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


    def move(self):
        
        self.flaptiming += 1 * dt
        if self.flaptiming >= self.flapspeed:
            self.flaptiming = 0
            self.velo += self.flapforce
            self.dirrection +=  (self.moy(50) - self.dirrection) / 10
            #self.pos += (self.moypos(100) - self.pos)
            
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
        self.poly.draw(self.pos, self.dirrection)

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

        scene.addboid(Boid(Vector2(random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1])), 100, 20, random.randint(0, 90) ))


    screen.fill(0)
    scene.upd()
    pygame.display.flip()



