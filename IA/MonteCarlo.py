#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:filename: MonteCarlo.py
:author:   Rodrigues Lucas
:version:  0.1
:summary:  Implementation of a AI monte carlo.


-------------------------------------------------------------------------

Copyright (C) 2023 Rodrigues Lucas

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

--------
"""

import os.path
from random import random
import json


class IAMonteCarlo:

    def __init__(self, nbSticks, qJsonPath, piJsonPath):
        self.__nbSticks = nbSticks
        self.__qJsonPath = qJsonPath
        self.__piJsonPath = piJsonPath

        if os.path.exists(qJsonPath):
            with open(qJsonPath, "r") as qJson:
                qJson = json.load(qJson)
            if len(qJson) == 0:
                self.__q = [0, 0]
                self.__q.append([0, 0, 0] * nbSticks - 2)
            else:
                self.__q = qJson

        if os.path.exists(piJsonPath):
            with open(piJsonPath, "r") as piJson:
                piJson = json.load(piJson)
            if len(piJson) == 0:
                self.__pi = [[0, 0]]
                self.__pi.append([0, 0, 0] * nbSticks - 2)
            else:
                self.__pi = piJson

        self.__movesPlay = [[0, 0]]
        self.__movesPlay.append([0, 0, 0] * nbSticks - 2)

        self.__nbGame = 0
        self.__epsilon = 0.8

    def action_choice(self, s):
        if s == 1:
            return 1

        movePlay = None
        while movePlay is None:
            randomNumber = random()

            if randomNumber <= self.__pi[s][0]:
                self.__movesPlay[s][0] = 1
                print("choice 1")
                movePlay = 1
            elif randomNumber <= self.__pi[s][0] + self.__pi[s][1]:
                self.__movesPlay[s][1] = 1
                print("choice 2")
                movePlay = 2
            elif len(self.__pi[s]) > 2 and randomNumber <= self.__pi[s][0] + self.__pi[s][1] + self.__pi[s][2]:
                self.__movesPlay[s][2] = 1
                print("choice 3")
                movePlay = 3

        return movePlay

    def uptade(self, result):
        self.__nbGame += 1
        if not result:
            for i in range(len(self.__movesPlay)):
                for j in range(len(self.__movesPlay[i])):
                    if self.__movesPlay[i][j] == 1:
                        self.__movesPlay[i][j] = -1

        for i in range(self.__nbSticks):
            for j in range(len(self.__q)):
                self.__q[i][j] = self.__q[i][j] + 1 / self.__nbGame * (self.__movesPlay[i][j] - self.__q[i][j])

        for i in range(self.__nbSticks):
            for j in range(len(self.__q)):
                if self.__movesPlay[i][j] != 0:
                    if self.__q[i][j] == max(self.__q[i]):
                        self.__pi[i][j] = self.__epsilon / 3 + (1 - self.__epsilon)
                    else:
                        self.__pi[i][j] = self.__epsilon / 3

        self.__movesPlay = [0, 0]
        self.__movesPlay.append([0, 0, 0] * self.__nbSticks - 2)

        if self.__epsilon - 0.00016 > 0:
            self.__epsilon -= 0.00016

        with open(self.__qJsonPath, "w+") as qJson:
            qJson.write(json.dumps(self.__q))

        with open(self.__piJsonPath, "w+") as piJson:
            piJson.write(json.dumps(self.__pi))
