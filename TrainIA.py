# -*- coding: UTF-8 -*-
"""
:filename: TrainIA.py
:author:   Lucas RODRIGUES
:version:  0.1
:summary:  This program allows us to train ours NIM IA brains.

-------------------------------------------------------------------------

Copyright (C) 2023 Lucas RODRIGUES

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

from IA.NaiveIA import NaiveIA
from IA.MonteCarlo import IAMonteCarlo

# ---------------------------------------------------------------------------

NB_GAMES = 100000

# ---------------------------------------------------------------------------


def get_path(nameIA) -> str:
    return os.path.join("IA", "output", f"{nameIA}-Brain-Report.json")


def load_ia_brain(nameIA) -> dict:
    path = get_path(nameIA)

    if os.path.exists(path):
        with open(path) as file:
            brain = json.load(file)
    else:
        brain = None

    return brain


def launch_game(first_IA, second_IA) -> bool:
    sticks = 20

    # play a game
    while sticks > 0:
        # ia1 move
        sticks -= first_IA.play(sticks)

        # check if ia1 has lost
        if sticks <= 0:
            return False

        # ia2 move
        sticks -= second_IA.play(sticks)

    return True


if __name__ == '__main__':
    nameIA1 = input("Choose IA1 (Aleatoire, MonteCarloIA, NaiveIA) : ").strip()
    nameIA2 = input("Choose IA2 (Aleatoire, MonteCarloIA, NaiveIA) : ").strip()

    if nameIA1 == "MonteCarloIA":
        ia1 = IAMonteCarlo(load_ia_brain(nameIA1))
    elif nameIA1 == "NaiveIA":
        ia1 = NaiveIA(load_ia_brain(nameIA1))

    if nameIA2 == "MonteCarloIA":
        ia2 = IAMonteCarlo(load_ia_brain(nameIA2))
    elif nameIA2 == "NaiveIA":
        ia2 = NaiveIA(load_ia_brain(nameIA2))

    print("Computing in progress...")
    ia1_begin = True

    for i in range(NB_GAMES):
        if ia1_begin:
            ia1_win = launch_game(ia1, ia2)
        else:
            ia1_win = launch_game(ia2, ia1)

        ia1_begin = not ia1_begin

        ia1.update_stat(ia1_win)
        ia2.update_stat(not ia1_win)

    ia1.export_brain(get_path(nameIA1))
    ia2.export_brain(get_path(nameIA2))
