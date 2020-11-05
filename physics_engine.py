# -*- coding: utf-8 -*-
"""
Created on 

"""

import pygame, sys
from pygame.locals import *
import numpy

pygame.init()

WINDOWHEIGHT=600
WINDOWWIDTH=800

SURFACE = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))


class Box:
    def __init__(self, centerX, centerY, width, height):
        self.rect = pygame.Rect(centerX - width/2, centerY-height/2, width, height)

    def update(self):
        pygame.draw.rect(SURFACE, (255,0,0), self.rect)

box1 = Box(100,100,20,20)

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #if event.type = KEYDOWN:
        #    if event.key = KEY_Q:
        #        pygame.quit()
        #        sys.exit()
        
    box1.update()
    pygame.display.update()