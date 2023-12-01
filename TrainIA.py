import os
import json
from IA.NaiveIA import NaiveIA
from IA.MonteCarlo import IAMonteCarlo


def load_ia_brain(NameIA) -> dict:
    IA_BRAIN_PATH = os.path.join(f"IA", "output", f"{NameIA}-Brain-Report.json")

    if os.path.exists(IA_BRAIN_PATH):
        with open(IA_BRAIN_PATH) as file:
            brain = json.load(file)
    else:
        brain = None

    return brain


NameIA1 = input("Choose IA1 (Aleatoire, MonteCarloIA, NaiveAI")
NameIA2 = input("Choose IA1 (Aleatoire, MonteCarloIA, NaiveAI")

if PLAYER_MODE == "MonteCarloIA":
    ia = IAMonteCarlo(load_ia_brain())
elif PLAYER_MODE == "NaiveIA":
    ia = NaiveIA(load_ia_brain())

sticks = 20


