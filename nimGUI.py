# -*- coding: UTF-8 -*-
"""
:filename: nimGUI.py
:author:   Maxime MONTERIN, Lucas RODRIGUES, Florian LOPITAUX
:version:  0.1
:summary:  Implementation of a graphical user interface.
           This application allows to play to the Nim game against an IA.

-------------------------------------------------------------------------

Copyright (C) 2023 Florian LOPITAUX

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

import os
import json
import pygame
from IA.NaiveIA import NaiveIA
from IA.MonteCarlo import IAMonteCarlo


# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

NB_STICKS = 20
BASED_COLOR = pygame.Color(181, 146, 109)
COLOR_PLAYER_1 = "aqua"
COLOR_PLAYER_2 = "orange"
PLAYER_MODE = input("Choose your opponent (Player, NaiveIA, MonteCarloIA) : ")
if PLAYER_MODE == "NaiveIA":
    IA_BRAIN_PATH = os.path.join("IA", "output", f"{PLAYER_MODE}_VS_MonteCarloIA-Brain-Report.json")
else:
    IA_BRAIN_PATH = os.path.join("IA", "output", f"{PLAYER_MODE}_VS_NaiveIA-Brain-Report.json")

# ---------------------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------------------


def initialize_sticks() -> list:
    sticks_coordinates = list()
    space_between_sticks = 150

    for _ in range(NB_STICKS):
        sticks_coordinates.append((BASED_COLOR, space_between_sticks))
        space_between_sticks += 50

    return sticks_coordinates


def draw_end_screen(surface: pygame.Surface, is_player_one_win: bool) -> None:
    # draw text
    jsonia = load_ia_brain()
    improving = f"Stats of \"{PLAYER_MODE}\" : \n"
    newxytext = 0

    font = pygame.font.SysFont('Comic Sans MS', 60)
    text_player_won = font.render(f"{'You' if is_player_one_win else 'The IA'} won !", True, (255, 255, 255))

    # add brain content on the end screen text
    for keys, values in jsonia.items():
        if keys != "brain":
            improving = improving + f"{keys} : {values} \n"

    # draw statistics of the current IA
    for ligne in improving.splitlines():
        ligne = font.render(ligne, True, (255, 255, 255))
        x = surface.get_rect().w / 2 - ligne.get_rect().w / 2
        y = surface.get_rect().h / 2 - ligne.get_rect().h

        surface.blit(ligne, (x, y + newxytext))

        newxytext += 50

    # draw the winner of the game
    x = surface.get_rect().w / 2 - text_player_won.get_rect().w / 2
    y = surface.get_rect().h / 2 - text_player_won.get_rect().h

    surface.blit(text_player_won, (x, y - 150))


def load_ia_brain() -> dict:
    if os.path.exists(IA_BRAIN_PATH):
        with open(IA_BRAIN_PATH) as file:
            brain = json.load(file)
    else:
        brain = None

    return brain


# ---------------------------------------------------------------------------
# INITIALIZATION
# ---------------------------------------------------------------------------

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Jeu de NIM")

pygame.font.init()
clock = pygame.time.Clock()

is_player_one_turn = True
win_text = None
coordinates = initialize_sticks()
stick_to_delete = -1

if PLAYER_MODE == "MonteCarloIA":
    ia = IAMonteCarlo(load_ia_brain())
elif PLAYER_MODE == "NaiveIA":
    ia = NaiveIA(load_ia_brain())


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

        # the game is finished
        if len(coordinates) == 0:
            # respawn sticks when the player pressed the 'y' or close if 'n'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    coordinates = initialize_sticks()
                elif event.key == pygame.K_n:
                    running = False

        else:
            # IA play
            if not is_player_one_turn and PLAYER_MODE != "Player":
                stick_to_delete = ia.play(len(coordinates)) - 1

            else:
                # check the size of the list to avoid an out of range
                if len(coordinates) >= 3:
                    max_range = 3
                else:
                    max_range = len(coordinates)

                # check if the user hovers a stick to change it's color
                for i in range(max_range):
                    if 220 <= pygame.mouse.get_pos()[1] <= 520 and \
                            coordinates[i][1] <= pygame.mouse.get_pos()[0] <= coordinates[i][1] + 25:

                        # print(f"stick n°{i + 1} hovered !")

                        # change color for all the sticks the user want to take
                        for j in range(i + 1):
                            if is_player_one_turn:
                                coordinates[j] = COLOR_PLAYER_1, coordinates[j][1]
                            else:
                                coordinates[j] = COLOR_PLAYER_2, coordinates[j][1]

                        # event if the user click
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            # print(f"click on the stick n°{i + 1}")
                            stick_to_delete = i

                    # reset color if the user doesn't hover the stick
                    else:
                        coordinates[i] = BASED_COLOR, coordinates[i][1]

            # delete the stick if the user or the ia click on it
            if stick_to_delete != -1:
                print("coup choisi", stick_to_delete + 1)
                # user can only pick sticks from the start of the list
                # user can only pick 1, 2, or 3 sticks max
                for j in range(stick_to_delete, -1, -1):
                    print("remove n°", j)
                    coordinates.pop(j)

                stick_to_delete = -1
                is_player_one_turn = not is_player_one_turn

                if len(coordinates) == 0:
                    if PLAYER_MODE != "Player":
                        ia.update_stat(not is_player_one_turn)

                    print("press y (yes) or n (no) to restart the game")

    # ---------------------------------------------------------------------------
    # DRAW GAME
    # ---------------------------------------------------------------------------

    # clear all the screen with a black background
    screen.fill("black")

    if len(coordinates) == 0:
        # draw the winner text
        draw_end_screen(screen, is_player_one_turn)

    else:
        # draw all sticks on the screen
        for i in range(len(coordinates)):
            pygame.draw.rect(screen, coordinates[i][0], (coordinates[i][1], 220, 25, 300))

    # update the screen to display all we draw before
    pygame.display.flip()

    # ---------------------------------------------------------------------------

    # line to limit FPS to 60 frame/second
    clock.tick(120)


# export IA brain
if PLAYER_MODE != "Player":
    ia.export_brain(IA_BRAIN_PATH)

# close the game
pygame.quit()
