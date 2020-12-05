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
GRAVITY = 50.0
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
        if not self.isActive:
            pygame.draw.rect(SURFACE, WHITE, self.rect)
            return
        
        self.velY = self.velY + GRAVITY * 1.0 / SPEED
        self.velX = self.velX
        self.centerX = self.centerX + self.velX / SPEED
        self.centerY = self.centerY + self.velY / SPEED
        
        self.rect.centery = int(self.centerY)
        self.rect.centerx = int(self.centerX)
        if self.rect.bottom >= WINDOWHEIGHT:
            self.rect.bottom = WINDOWHEIGHT - 1
            self.centerX = self.rect.centerx
            self.centerY = self.rect.centery
            self.isActive = False
        pygame.draw.rect(SURFACE, WHITE, self.rect)

class Circle:
    def __init__(self, centerX, centerY, radius):
        self.rect = pygame.Rect(centerX - radius, centerY - radius, 2*radius, 2*radius)
        self.velX = float(random.randint(-20, 20))
        self.velY = float(random.randint(-20, 20))
        self.centerX = self.rect.centerx
        self.centerY = self.rect.centery
        self.radius = radius
        self.isActive = True

    def update(self):
        if not self.isActive:
            pygame.draw.circle(SURFACE, WHITE, (self.rect.centerx,self.rect.centery), self.radius)
            return
        
        self.velY = self.velY + GRAVITY * 1.0 / SPEED
        self.velX = self.velX
        self.centerX = self.centerX + self.velX / SPEED
        self.centerY = self.centerY + self.velY / SPEED
        
        self.rect.centery = int(self.centerY)
        self.rect.centerx = int(self.centerX)
        if self.rect.bottom >= WINDOWHEIGHT:
            self.rect.bottom = WINDOWHEIGHT - 1
            self.centerX = self.rect.centerx
            self.centerY = self.rect.centery
            self.isActive = False
        pygame.draw.circle(SURFACE, WHITE, (self.rect.centerx,self.rect.centery), self.radius)       

#boxes = []
circles = []
while True:

    SURFACE.fill(BLACK)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            #boxes.append(Box(pos[0], pos[1], 30, 30))
            circles.append(Circle(pos[0], pos[1], 30))
    
    #for box in boxes:
    #    box.update()
    for circle in circles:
        circle.update()
            
        #if event.type = KEYDOWN:
        #    if event.key = KEY_Q:
        #        pygame.quit()
        #        sys.exit()
    clock.tick(SPEED)       
    pygame.display.update()