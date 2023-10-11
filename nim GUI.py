#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 10:35:37 2023

@author: m21202745
"""

import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Jeu de NIM")
clock = pygame.time.Clock()
running = True
nbBaton = 20
espaceEntreLesBatons = 150
batonADelete = -1;
clickNumber = 3

coordinates = list()


for i in range (nbBaton):
    coordinates.append(("purple", espaceEntreLesBatons))
    espaceEntreLesBatons += 50

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for i in range(len(coordinates)):
            if(220 <= pygame.mouse.get_pos()[1] <= 520 and coordinates[i][1] <= pygame.mouse.get_pos()[0] <= coordinates[i][1] + 25):
                print("survol detecté sur le baton n°", i + 1)
                coordinates[i] = "aqua", coordinates[i][1]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("click detecté sur le baton n°", i + 1)
                    batonADelete = i 
            else:
                coordinates[i] = "purple", coordinates[i][1]
        if(batonADelete != -1) :
            del coordinates[batonADelete]
            batonADelete = -1

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    for i in range (len(coordinates)):
        pygame.draw.rect(screen, coordinates[i][0], (coordinates[i][1], 220, 25, 300))
    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(120)  # limits FPS to 60

pygame.quit()
 