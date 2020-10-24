# -*- coding: utf-8 -*-
"""
Created on 

"""

import pygame, sys
from pygame.locals import *

pygame.init()

WINDOWHEIGHT=600
WINDOWWIDTH=800

SURFACE = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()