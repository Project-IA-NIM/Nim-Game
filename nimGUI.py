# -*- coding: UTF-8 -*-
"""
:filename: nimGUI.py
:author:   Maxime Monterin
:version:  0.1
:summary:  Implementation of a graphical user interface.
           This application allows to play to the Nim game against an IA.

-------------------------------------------------------------------------

Copyright (C) 2023 Maxime Monterin

Use of this software is governed by the GNU Public License, version 3.

Project-IA-Nim is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Project-IA-Nim is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Project-IA-Nim. If not, see <http://www.gnu.org/licenses/>.

This banner notice must not be removed.

-------------------------------------------------------------------------
"""

import pygame

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

NB_STICKS = 20
MAX_CLICK_COUNT = 3

# ---------------------------------------------------------------------------
# INITIALIZATION
# ---------------------------------------------------------------------------

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Jeu de NIM")

clock = pygame.time.Clock()

stick_to_delete = -1
space_between_sticks = 150

coordinates = list()

for i in range(NB_STICKS):
    coordinates.append(("purple", space_between_sticks))
    space_between_sticks += 50

# ---------------------------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------------------------
running = True

while running:
    
    # ---------------------------------------------------------------------------
    # UPDATE GAME
    # ---------------------------------------------------------------------------

    for event in pygame.event.get():
        # event when the user close the window to stop the program
        if event.type == pygame.QUIT:
            running = False

        # check if the user hovers a stick to change it's color
        for i in range(len(coordinates)):
            if(220 <= pygame.mouse.get_pos()[1] <= 520 and coordinates[i][1] <= pygame.mouse.get_pos()[0] <= coordinates[i][1] + 25):
                print(f"stick n°{i + 1} hovered !")
                coordinates[i] = "aqua", coordinates[i][1]

                # event if the user click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(f"click on the stick n°{i + 1}")
                    stick_to_delete = i
            
            # reset color if the user doesn't hover the stick
            else:
                coordinates[i] = "purple", coordinates[i][1]

        # delete the stick if the user click on it
        if(stick_to_delete != -1) :
            del coordinates[stick_to_delete]
            stick_to_delete = -1

    # ---------------------------------------------------------------------------
    # DRAW GAME
    # ---------------------------------------------------------------------------

    # clear all the screen with a black background
    screen.fill("black")

    # draw all sticks on the screen
    for i in range(NB_STICKS):
        pygame.draw.rect(screen, coordinates[i][0], (coordinates[i][1], 220, 25, 300))

    # update the screen to display all we draw before
    pygame.display.flip()

    # ---------------------------------------------------------------------------

    # line to limit FPS to 60 frame/second
    clock.tick(120)

# close the game
pygame.quit()
