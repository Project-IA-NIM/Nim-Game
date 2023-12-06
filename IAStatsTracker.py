# -*- coding: UTF-8 -*-
"""
:filename: IAStatsTracker.py
:author:   Florian Lopitaux
:version:  0.1
:summary:  Implementation of a tracker to analyse the comportment of our IA.

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

import json
import os.path

from IA.NaiveIA import NaiveIA
from IA.MonteCarlo import IAMonteCarlo

# ---------------------------------------------------------------------------


class IAStatsTracker:

    # ---------------------------------------------------------------------------
    # CONSTRUCTOR
    # ---------------------------------------------------------------------------

    def __init__(self, validate_cursor: float = .90) -> None:
        self.__naiveIA_stats = list()
        self.__monteCarloIA_stats = list()

        self.__validate_cursor = validate_cursor

    # ---------------------------------------------------------------------------
    # GETTERS
    # ---------------------------------------------------------------------------

    def get_naiveIA_stats(self) -> list:
        return self.__naiveIA_stats
    
    # ---------------------------------------------------------------------------
    
    def get_monteCarloIA_stats(self) -> list:
        return self.__monteCarloIA_stats

    # ---------------------------------------------------------------------------
    # PUBLIC METHODS
    # ---------------------------------------------------------------------------

    def update_stats(self, ia) -> None:
        nb_correct_moves_found = 0

        if isinstance(ia, NaiveIA):
            ia_brain = ia.get_brain()

            for nb_sticks, plays in ia_brain.items():
                nb_sticks = int(nb_sticks)
                correct_move = nb_sticks % 4 - 1

                # no correct moves to play (5, 9, 13, ... sticks remaining)
                if correct_move == 0:
                    continue
                elif correct_move == -1:
                    correct_move = 3

                # check if move property exceed the validate cursor
                if plays[correct_move - 1][1] >= self.__validate_cursor:
                    nb_correct_moves_found += 1

            self.__naiveIA_stats.append(nb_correct_moves_found)

        elif isinstance(ia, IAMonteCarlo):
            ia_brain = ia.get_brain()

            for i in range(len(ia_brain)):
                nb_sticks = i + 2
                correct_move = nb_sticks % 4 - 1

                # no correct moves to play (5, 9, 13, ... sticks remaining)
                if correct_move == 0:
                    continue
                elif correct_move == -1:
                    correct_move = 3

                if ia_brain[i][correct_move - 1] >= self.__validate_cursor:
                    nb_correct_moves_found += 1
            
            self.__monteCarloIA_stats.append(nb_correct_moves_found)

    # ---------------------------------------------------------------------------

    def export_stats(self, filename: str) -> None:
        with open(os.path.join("IA", "output", f"{filename}.json"), 'w') as output_file:
            json_export = dict()

            if len(self.__naiveIA_stats) > 0:
                json_export['NaiveIA'] = self.__naiveIA_stats

            if len(self.__monteCarloIA_stats) > 0:
                json_export['MonteCarloIA'] = self.__monteCarloIA_stats

            output_file.write(json.dumps(json_export, indent=3))
