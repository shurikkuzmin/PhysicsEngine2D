# -*- coding: utf-8 -*-
"""
Created on 

"""

import pygame, sys
from pygame.locals import *
import numpy
import random

pygame.init()

WINDOWHEIGHT=600
WINDOWWIDTH=800
SPEED = 100
SPEEDGIF = 10
GRAVITY = 20.0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

SURFACE = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))


class PhysicalObject:
    def __init__(self, centerX, centerY, mass, k, velX, velY):
        self.velX = velX
        self.velY = velY
        self.centerX = centerX
        self.centerY = centerY
        self.mass = mass
        self.k = k
        
    def update(self):
        self.velY = self.velY + GRAVITY * 1.0 / SPEED
        self.velX = self.velX
        self.centerX = self.centerX + self.velX / SPEED
        self.centerY = self.centerY + self.velY / SPEED
        
        self.rect.centery = int(self.centerY)
        self.rect.centerx = int(self.centerX)
        
        self.draw()

class Box(PhysicalObject): 
    def __init__(self, centerX, centerY, width, height, mass, k, velX, velY):
        PhysicalObject.__init__(self, centerX, centerY, mass, k, velX, velY)
        self.rect = pygame.Rect(centerX - width/2, centerY-height/2, width, height)

    def draw(self):
        pygame.draw.rect(SURFACE, WHITE, self.rect)

class Circle(PhysicalObject):
    def __init__(self, centerX, centerY, radius, mass, k, velX, velY):
        PhysicalObject.__init__(self, centerX, centerY, mass, k, velX, velY)
        self.radius = radius
        self.rect = pygame.Rect(centerX - radius, centerY - radius, 2*radius, 2*radius)

    def draw(self):
        pygame.draw.circle(SURFACE, WHITE, (self.rect.centerx,self.rect.centery), self.radius)       

class Earth(Circle):
    def __init__(self, centerX, centerY, radius, mass, k, velX, velY):
        Circle.__init__(self, centerX, centerY, radius, mass, k, velX, velY)
 
    def update(self):
        self.velY = 0.0
        self.velX = 0.0
        self.draw()

def collision(obj1, obj2):
    x1 = obj1.centerX
    y1 = obj1.centerY
    x2 = obj2.centerX
    y2 = obj2.centerY
    
    isCollision = False
    if isinstance(obj1, Circle) and isinstance(obj2, Circle):
        dist = numpy.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        if dist < obj1.radius + obj2.radius:
            isCollision = True
            normX = (x1 - x2) / dist
            normY = (y1 - y2) / dist
    if (isinstance(obj1, Box) and isinstance(obj2, Box)) or (isinstance(obj1, Circle) and isinstance(obj2, Box)) or (isinstance(obj2, Circle) and isinstance(obj1, Box)):
        dist = numpy.sqrt((x1 - x2)**2 + (y1 - y2)**2)        
        w1 = 0
        h1 = 0
        w2 = 0
        h2 = 0
        if isinstance(obj1, Circle):
            w1 = abs((x2 - x1) / dist) * obj1.radius
            h1 = abs((y2 - y1) / dist) * obj1.radius
            # Shift the center
            x1 = obj1.centerX + 0.5 * w1 * numpy.sign(x2 - x1)
            y1 = obj1.centerY + 0.5 * h1 * numpy.sign(y2 - y1)
            w2 = obj2.rect.width
            h2 = obj2.rect.height
        elif isinstance(obj2, Circle):
            w2 = abs((x2 - x1) / dist) * obj2.radius
            h2 = abs((y2 - y1) / dist) * obj2.radius
            x2 = obj2.centerX + 0.5 * w2 * numpy.sign(x1 - x2)
            y2 = obj2.centerY + 0.5 * h2 * numpy.sign(y1 - y2)

            w1 = obj1.rect.width
            h1 = obj1.rect.height
        else:
            w1 = obj1.rect.width
            h1 = obj1.rect.height
            w2 = obj2.rect.width
            h2 = obj2.rect.height
        if abs(x2 - x1) <= 0.5 * (w1 + w2) and abs(y2 - y1) <= 0.5 * (h1 + h2):
            isCollision = True
            penetrationX = 0.5 * (w1 + w2) - abs(x2 - x1)
            penetrationY = 0.5 * (h1 + h2) - abs(y2 - y1)

            normX = 0.0
            normY = 0.0
            if penetrationY > penetrationX:
                # Normal will be parallel to X
                if x2 > x1:
                    normX = -1.0
                    normY = 0.0
                else:
                    normX = 1.0
                    normY = 0.0
            else:
                # Normal will be parallel to Y
                if y2 > y1:
                    normX = 0.0
                    normY = -1.0
                else:
                    normX = 0.0
                    normY = 1.0
        
    if isCollision:
        velX1 = obj1.velX
        velY1 = obj1.velY
        velX2 = obj2.velX
        velY2 = obj2.velY
      
        dotProduct = (velX1 - velX2) * normX + (velY1 - velY2) * normY
        if dotProduct < 0.0:
            m1 = obj1.mass
            m2 = obj2.mass        

            k = min(obj1.k, obj2.k)
            impulse = - m1 * m2 / (m1 + m2) * (1.0 + k) * dotProduct
            obj1.velX += impulse * normX / m1
            obj1.velY += impulse * normY / m1
            obj2.velX -= impulse * normX / m2
            obj2.velY -= impulse * normY / m2



earth = Earth(WINDOWWIDTH/2,4*WINDOWHEIGHT,3*WINDOWHEIGHT+40, 1000.0, 0.2, 0.0, 0.0)
circle1 = Circle(WINDOWWIDTH/2 - 100, WINDOWHEIGHT/2 - 10, 30, 5.0, 1.0, 30.0, 0.0)
circle2 = Circle(WINDOWWIDTH/2 + 150, WINDOWHEIGHT/2, 10, 1.0, 1.0, -30.0, 0.0)
circle3 = Circle(WINDOWWIDTH/2 - 100, WINDOWHEIGHT/2 - 100, 30, 5.0, 1.0, 20.0, 20.0)
circle4 = Circle(WINDOWWIDTH/2 + 100, WINDOWHEIGHT/2 - 120, 30, 5.0, 1.0, -20.0, 0.0)
box1 = Box(WINDOWWIDTH/2 - 200, WINDOWHEIGHT/2 - 10, 30, 30, 1.0, 1.0, 30.0, 0.0)
box2 = Box(WINDOWWIDTH/2 + 100, WINDOWHEIGHT/2, 30, 30, 1.0, 1.0, -30.0, 0.0)
box3 = Box(WINDOWWIDTH/2 + 20, WINDOWHEIGHT/2 - 60, 30, 30, 1.0, 1.0, 0.0, -20.0)

objects = [earth, circle1, circle2, circle3, circle4, box1, box2, box3]

counter = 0
isGif = False
if isGif:
    import os
    import glob
    for png in glob.glob("*.png"):
        os.remove(png)

isRunning = True
while isRunning:

    SURFACE.fill(BLACK)
    for event in pygame.event.get():
        if event.type == QUIT:
            isRunning = False
    
    for obj in objects:
        obj.update()
        
    for i in range(0, len(objects)):
        for j in range(i + 1, len(objects)):
            collision(objects[i], objects[j])


    counter = counter + 1
    if isGif:
        if counter % (SPEED/SPEEDGIF) == 0:
            fileName = "image{:05d}".format(counter) + ".png"
            pygame.image.save(SURFACE, fileName)

    clock.tick(SPEED)       
    pygame.display.update()
    
if isGif:
    import PIL
    frames = []
    images = glob.glob("*.png")
    for image in images:
        frame = PIL.Image.open(image)
        frames.append(frame)
    frames[0].save("animated.gif", format="GIF", append_images=frames[1:], save_all=True, duration=60, loop=0)
    
pygame.quit()
sys.exit()
