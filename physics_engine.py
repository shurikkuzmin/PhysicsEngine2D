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
SPEED = 60
GRAVITY = 20.0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

SURFACE = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))


class Box:
    def __init__(self, centerX, centerY, width, height):
        self.rect = pygame.Rect(centerX - width/2, centerY-height/2, width, height)
        self.velX = float(random.randint(-20, 20))
        self.velY = float(random.randint(-20, 20))
        self.centerX = self.rect.centerx
        self.centerY = self.rect.centery
        self.isActive = True

    def update(self):
        #if not self.isActive:
        #    pygame.draw.rect(SURFACE, WHITE, self.rect)
        #    return

        self.velY = self.velY + GRAVITY * 1.0 / SPEED
        self.velX = self.velX
        self.centerX = self.centerX + self.velX / SPEED
        self.centerY = self.centerY + self.velY / SPEED
        
        self.rect.centery = int(self.centerY)
        self.rect.centerx = int(self.centerX)
        #if self.rect.bottom >= WINDOWHEIGHT:
        #    self.rect.bottom = WINDOWHEIGHT - 1
        #    self.centerX = self.rect.centerx
        #    self.centerY = self.rect.centery
        #    #self.isActive = False
        pygame.draw.rect(SURFACE, WHITE, self.rect)

class Circle:
    def __init__(self, centerX, centerY, radius, mass, k, velX, velY):
        self.rect = pygame.Rect(centerX - radius, centerY - radius, 2*radius, 2*radius)
        self.velX = velX #float(random.randint(-20, 20))
        self.velY = velY #float(random.randint(-20, 20))
        self.centerX = self.rect.centerx
        self.centerY = self.rect.centery
        self.radius = radius
        self.mass = mass
        self.k = k 
        self.isActive = True

    def update(self):
        
        self.velY = self.velY + GRAVITY * 1.0 / SPEED
        self.velX = self.velX
        self.centerX = self.centerX + self.velX / SPEED
        self.centerY = self.centerY + self.velY / SPEED
        
        self.rect.centery = int(self.centerY)
        self.rect.centerx = int(self.centerX)
        pygame.draw.circle(SURFACE, WHITE, (self.rect.centerx,self.rect.centery), self.radius)       

def collisionCircles(i, j, circles):
    dist = numpy.sqrt((circles[i].centerX - circles[j].centerX)**2 + (circles[i].centerY - circles[j].centerY)**2)
    if dist < circles[i].radius + circles[j].radius:
        x1 = circles[i].centerX
        y1 = circles[i].centerY
        x2 = circles[j].centerX
        y2 = circles[j].centerY
        velX1 = circles[i].velX
        velY1 = circles[i].velY
        velX2 = circles[j].velX
        velY2 = circles[j].velY
        m1 = circles[i].mass
        m2 = circles[j].mass        
        normX = (x1 - x2) / dist
        normY = (y1 - y2) / dist
        dotProduct = (velX1 - velX2) * normX + (velY1 - velY2) * normY
        if dotProduct < 0.0:
            k = min(circles[i].k, circles[j].k)
            impulse = - m1 * m2/(m1 + m2) * (1.0 + k) * dotProduct
            circles[i].velX += impulse * normX / m1
            circles[i].velY += impulse * normY / m1
            circles[j].velX -= impulse * normX / m2
            circles[j].velY -= impulse * normY / m2

earth = Circle(WINDOWWIDTH/2,4*WINDOWHEIGHT,3*WINDOWHEIGHT+40,10000.0, 0.2, 0.0, 0.0)
circle1 = Circle(WINDOWWIDTH/2 - 100, WINDOWHEIGHT/2 - 10, 30, 5.0, 1.0, 30.0, 0.0)
circle2 = Circle(WINDOWWIDTH/2 + 100, WINDOWHEIGHT/2, 10, 1.0, 1.0, -30.0, 0.0)
circle3 = Circle(WINDOWWIDTH/2 - 100, WINDOWHEIGHT/2 - 100, 30, 5.0, 1.0, 20.0, 20.0)
circle4 = Circle(WINDOWWIDTH/2 + 100, WINDOWHEIGHT/2 - 120, 30, 5.0, 1.0, -20.0, 0.0)

circles = [earth, circle1, circle2, circle3, circle4]
while True:

    SURFACE.fill(BLACK)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #if event.type == MOUSEBUTTONUP:
        #    pos = pygame.mouse.get_pos()
        #    circles.append(Circle(pos[0], pos[1], 30))
    
    #for box in boxes:
    #    box.update()
    for i in range(0, len(circles)):
        for j in range(i + 1, len(circles)):
            collisionCircles(i, j, circles)
            #circles[i] collision with circles[j] 
        
    for circle in circles[1:]:
        circle.update()
    pygame.draw.circle(SURFACE, WHITE, (earth.rect.centerx,earth.rect.centery), earth.radius) 
        #if event.type = KEYDOWN:
        #    if event.key = KEY_Q:
        #        pygame.quit()
        #        sys.exit()
    clock.tick(SPEED)       
    pygame.display.update()