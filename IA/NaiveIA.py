# -*- coding: UTF-8 -*-
"""
:filename: NaiveIA.py
:author:   Florian Lopitaux
:version:  1.0
:summary:  Implementation of an IA for the Nim game.
           Naive approach of the algorithm used by this IA.

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

import os
import json
import random


# ---------------------------------------------------------------------------

class NaiveIA:

    # ---------------------------------------------------------------------------
    # CONSTRUCTOR
    # ---------------------------------------------------------------------------

    def __init__(self, imported_json_brain: dict = None, update_coef: float = 0.02) -> None:
        if imported_json_brain is None:
            # initialize IA brain with default value
            self.__brain = self.__create_default_brain()
            self.__nbGames = 0
            self.__nbWin = 0

        else:
            # initialize IA brain with an existing brain
            self.__brain = imported_json_brain['brain']
            self.__nbGames = imported_json_brain['nb_games_played']
            self.__nbWin = imported_json_brain['nb_games_won']

        # list of plays during the current game
        self.__currentPlay = list()

        # coefficient apply when the IA updates the probabilities at the end of the game
        self.__update_coef = update_coef

    # ---------------------------------------------------------------------------
    # GETTERS
    # ---------------------------------------------------------------------------

    def get_brain(self) -> dict:
        return self.__brain

    # ---------------------------------------------------------------------------
    # PUBLIC METHODS
    # ---------------------------------------------------------------------------

    def export_brain(self, export_file_path: str = None) -> None:
        # default file path
        if export_file_path is None:
            export_file_path = os.path.join("output", "NaiveIA-Brain-Report.json")

        if self.__nbGames == 0:
            # no game played, so we set to 0 (we can't divide by 0 !)
            win_rate = 0
            lose_rate = 0
        else:
            win_rate = round((self.__nbWin / self.__nbGames) * 100, 2)
            lose_rate = round(((self.__nbGames - self.__nbWin) / self.__nbGames) * 100, 2)

        # export brain in json format in an output file
        export_brain = {
            "nb_games_played": self.__nbGames,
            "nb_games_won": self.__nbWin,
            "nb_games_lost": self.__nbGames - self.__nbWin,
            "win_rate": win_rate,
            "lose_rate": lose_rate,

            "brain": self.__brain
        }

        with open(export_file_path, 'w') as output_file:
            json_brain = json.dumps(export_brain, indent=3)
            output_file.write(json_brain)

    # ---------------------------------------------------------------------------

    def play(self, nb_stick_remaining: int) -> int:
        # only one play possible
        if nb_stick_remaining == 1:
            return 1

        # convert in string to corresponds with the brain format (dictionnary keys in string)
        nb_stick_remaining = str(nb_stick_remaining)
        ia_play = None

        # choosing current play depending on play probabilities
        while ia_play is None:
            random_number = random.random()

            # check probability to play only stick
            if random_number < self.__brain[nb_stick_remaining][0][1]:
                ia_play = 1
                break
            else:
                random_number -= self.__brain[nb_stick_remaining][0][1]

            # check probability to play two sticks
            if random_number < self.__brain[nb_stick_remaining][1][1]:
                ia_play = 2
                break
            else:
                random_number -= self.__brain[nb_stick_remaining][1][1]

            # check probability to play three sticks
            if len(self.__brain[nb_stick_remaining]) >= 3 and random_number < self.__brain[nb_stick_remaining][2][1]:
                ia_play = 3

        # add the current play in the list to update the probabilities at the end of the game
        self.__currentPlay.append((nb_stick_remaining, ia_play))

        return ia_play

    # ---------------------------------------------------------------------------

    def update_stat(self, has_won: bool) -> None:
        # update ia stats
        self.__nbGames += 1

        if has_won:
            percent_update = self.__update_coef
            self.__nbWin += 1
        else:
            percent_update = -self.__update_coef

        # update plays probabilities
        for play in self.__currentPlay:
            for possibility in self.__brain[play[0]]:
                if possibility[0] == play[1]:
                    # update the probability of the play played during the game
                    self.__brain[play[0]][possibility[0] - 1][1] += percent_update
                else:
                    # update the probability of the other plays
                    self.__brain[play[0]][possibility[0] - 1][1] -= percent_update / (len(self.__brain[play[0]]) - 1)

                # limit maximum and minimum probabilities
                if self.__brain[play[0]][possibility[0] - 1][1] > 0.98:
                    self.__brain[play[0]][possibility[0] - 1][1] = 0.98

                elif self.__brain[play[0]][possibility[0] - 1][1] < 0.01:
                    self.__brain[play[0]][possibility[0] - 1][1] = 0.01

        # reset current plays to the next game
        self.__currentPlay.clear()

    # ---------------------------------------------------------------------------
    # PRIVATE METHODS
    # ---------------------------------------------------------------------------

    def __create_default_brain(self) -> dict:
        brain = dict()

        # only 2 plays possible when that remaining only 2 sticks
        brain["2"] = [
            [1, 0.5],
            [2, 0.5]
        ]

        for i in range(3, 21):
            brain[str(i)] = [
                [1, 0.33],
                [2, 0.33],
                [3, 0.33]
            ]

        return brain
