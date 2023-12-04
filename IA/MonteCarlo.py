#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:filename: MonteCarlo.py
:author:   Lucas RODRIGUES, Florian Lopitaux
:version:  0.2
:summary:  Implementation of an IA for the Nim game.
           Monte Carlo approach of the algorithm used by this IA.

-------------------------------------------------------------------------

Copyright (C) 2023 Florian Lopitaux

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

import os.path
import json
from random import random


# ---------------------------------------------------------------------------

class IAMonteCarlo:

    # ---------------------------------------------------------------------------
    # CONSTRUCTOR
    # ---------------------------------------------------------------------------

    def __init__(self, imported_json_brain: dict = None):
        self.__nb_sticks = 20

        self.__moves_play = self.__create_default_list()

        if imported_json_brain is None:
            self.__nb_games = 0
            self.__nb_win = 0
            self.__epsilon = 0.8

            self.__q = self.__create_default_list()

            self.__pi = list()
            self.__pi.append([.5, .5])

            for i in range(self.__nb_sticks - 2):
                self.__pi.append([.33, .33, .33])

        else:
            self.__nb_games = imported_json_brain['nb_games_played']
            self.__nb_win = imported_json_brain['nb_games_won']
            self.__epsilon = imported_json_brain['current_epsilon']

            self.__q = imported_json_brain['q']
            self.__pi = imported_json_brain['pi']

    # ---------------------------------------------------------------------------
    # PUBLIC METHODS
    # ---------------------------------------------------------------------------

    def export_brain(self, export_file_path: str = None) -> None:
        # default file path
        if export_file_path is None:
            export_file_path = os.path.join("output", "IAMonteCarlo-Brain-Report.json")

        if self.__nb_games == 0:
            # no game played, so we set to 0 (we can't divide by 0 !)
            win_rate = 0
            lose_rate = 0
        else:
            win_rate = round((self.__nb_win / self.__nb_games) * 100, 2)
            lose_rate = round(((self.__nb_games - self.__nb_win) / self.__nb_games) * 100, 2)

        # export brain in json format in an output file
        export_brain = {
            "nb_games_played": self.__nb_games,
            "nb_games_won": self.__nb_win,
            "nb_games_lost": self.__nb_games - self.__nb_win,
            "win_rate": win_rate,
            "lose_rate": lose_rate,

            "current_epsilon": self.__epsilon,
            "q": self.__q,
            "pi": self.__pi
        }

        with open(export_file_path, "w") as output_file:
            json_brain = json.dumps(export_brain, indent=3)
            output_file.write(json_brain)

    # ---------------------------------------------------------------------------

    def play(self, nb_stick_remaining: int) -> int:
        if nb_stick_remaining == 1:
            return 1

        nb_stick_remaining -= 2
        move_play = None

        while move_play is None:
            random_number = random()

            # check probability to play only stick
            if random_number <= self.__pi[nb_stick_remaining][0]:
                move_play = 1
                break
            else:
                random_number -= self.__pi[nb_stick_remaining][0]

            # check probability to play two sticks
            if random_number <= self.__pi[nb_stick_remaining][1]:
                move_play = 2
                break
            else:
                random_number -= self.__pi[nb_stick_remaining][1]

            # check probability to play three sticks
            if len(self.__pi[nb_stick_remaining]) > 2 and random_number <= self.__pi[nb_stick_remaining][2]:
                move_play = 3

        # add the current play in the list to update the probabilities at the end of the game
        self.__moves_play[nb_stick_remaining][move_play - 1] = 1

        return move_play

    # ---------------------------------------------------------------------------

    def update_stat(self, has_won: bool) -> None:
        self.__nb_games += 1

        if has_won:
            self.__nb_win += 1

        for i in range(len(self.__q)):
            for j in range(len(self.__q[i])):
                if not has_won:
                    self.__moves_play[i][j] *= -1

                self.__q[i][j] += 1 / self.__nb_games * (self.__moves_play[i][j] - self.__q[i][j])

        for i in range(len(self.__q)):
            for j in range(len(self.__q[i])):
                self.__pi[i][j] = self.__epsilon / 3

                if self.__q[i][j] == max(self.__q[i]):
                    self.__pi[i][j] += 1 - self.__epsilon

        self.__moves_play = self.__create_default_list()

        if self.__epsilon - 0.00016 >= 0:
            self.__epsilon -= 0.00016
        else:
            self.__epsilon = 0

    # ---------------------------------------------------------------------------
    # PRIVATE METHODS
    # ---------------------------------------------------------------------------

    def __create_default_list(self) -> list:
        brain = list()

        # only 2 plays possible when that remaining only 2 sticks
        brain.append([0, 0])

        # create empty brain
        for i in range(self.__nb_sticks - 2):
            brain.append([0, 0, 0])

        return brain
