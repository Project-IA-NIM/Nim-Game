# -*- coding: UTF-8 -*-
"""
:filename: modelization.py
:author:   Lucas RODRIGUES, Florian LOPITAUX
:version:  0.1
:summary:  Implementation of a matplotlib graphics for our IA.

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

import os.path
import json
import re
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------


def create_graphic(stats: dict, name_IA: str) -> None:
    y = stats[name_IA]
    x = [i for i in range(len(y))]

    each_nb_points = int(len(y) / 200)

    plt.plot(x[::each_nb_points], y[::each_nb_points])
    plt.title(f"Nombre de bon coups trouvé par {name_IA}")
    plt.xlabel("Nombre de parties jouées")
    plt.ylabel("Nombre de bon coups trouvé")
    plt.show()


if __name__ == '__main__':
    stat_files = list()

    # get all ia stats files
    directory = os.path.join("IA", "output")

    for root, dirs, files in os.walk(directory):
        for file in files:
            if re.match("^stats_.*\.json$", file):
                stat_files.append(os.path.join(root, file))

    # user choose ia stat file
    for i in range(len(stat_files)):
        print(f" - {i}: {stat_files[i]}")

    file_choice = int(input("Choose statistic file (0, 1, 2, ...) : "))

    # get ia stats
    with open(stat_files[file_choice]) as output_file:
        ia_stats = json.loads(output_file.read())

    # show NaiveIA graphic
    if ia_stats.get("NaiveIA") is not None:
        create_graphic(ia_stats, "NaiveIA")

    # show MonteCarloIA graphic
    if ia_stats.get("MonteCarloIA") is not None:
        create_graphic(ia_stats, "MonteCarloIA")
