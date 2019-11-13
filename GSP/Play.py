
from random import *

DEFENSE = {
    "Base": {
        "Stuff": 7,
        "Rush": 4,
        "Cover": 7
    },

    "Nickel": {
        "Stuff": 6,
        "Rush": 4,
        "Cover": 8
    },

    "Dime": {
        "Stuff": 5,
        "Rush": 4,
        "Cover": 9
    },

    "Blitz": {
        "Stuff": 7,
        "Rush": 5,
        "Cover": 6
    }
}


def SimulateRun(defscheme, yardline):
    gained = randint(2, 12) - randint(0, DEFENSE[defscheme]["Stuff"])
    event = None
    if gained < -2:
        gained = -2

    if gained < 0:
        event = "TFL"
    else:
        event = "run"

    print("Yards Gained: {}".format(gained))

    return gained, event, ""


def SimulateShortPass(defscheme, yardline):
    gained = 0
    event = None
    result = ""

    # no sacks

    if random() < 0.85 - (0.03 * DEFENSE[defscheme]["Cover"]):
        gained = randint(2, 10)
        event = "complete"
        print("Pass complete for {} yards".format(gained))
    elif random() < 0.02 + (0.01 * DEFENSE[defscheme]["Cover"]):
        event = "interception"
        result = "interception"
        print("Pass intercepted")
    else:
        event = "incomplete"
        print("Pass incomplete")

    return gained, event, result


def SimulatePass(defscheme, yardline):
    gained = 0
    event = ""
    result = ""

    if random() < 0.05 * (DEFENSE[defscheme]["Rush"] - 3):  # sack
        gained = randint(-8, 0)
        event = "sack"
        print("Sack")
    elif random() < 0.90 - (0.05 * DEFENSE[defscheme]["Cover"]):
        gained = randint(4, 20)
        event = "complete"
        print("Pass complete for {} yards".format(gained))
    elif random() < 0.03 + (0.015 * DEFENSE[defscheme]["Cover"]):
        event = "interception"
        result = "interception"
        print("Pass intercepted")
    else:
        event = "incomplete"
        print("Pass incomplete")

    return gained, event, result


def SimulateDeepPass(defscheme, yardline):
    gained = 0
    event = ""
    result = ""

    if random() < 0.06 * (DEFENSE[defscheme]["Rush"] - 3):
        gained = randint(-8, 0)
        event = "sack"
        print("Sack")
    elif random() < 0.80 - (0.06 * DEFENSE[defscheme]["Cover"]):
        gained = randint(20, 80)
        event = "complete"
        print("Pass complete for {} yards".format(gained))
    elif random() < 0.03 + (0.015 * DEFENSE[defscheme]["Cover"]):
        event = "interception"
        result = "interception"
        print("Pass intercepted")
    else:
        event = "incomplete"
        print("Pass incomplete")

    return gained, event, result


def SimulatePunt(defscheme, yardline):
    gained = 30 + randint(0, 25)
    print("Punt for {} yards".format(gained))

    return gained, "", "punt"


def SimulateFGA(defscheme, yardline):
    fromYds = 100 - yardline + 17
    result = "MISS"
    if random() < (0.95 - 0.01 * (fromYds - 17)):
        result = "GOOD"

    print("Attempted FG from {} yards: {}".format(fromYds, result))

    if result == "GOOD":
        return 0, "", "FGM"
    else:
        return 0, "", "missed FG"


def SimulatePlay(playcall, defcall, yardline):
    print("Playcall: ", playcall)
    print("Defense: ", defcall)

    gained, event, result = globals()["Simulate" + playcall](defcall, yardline)

    if not result:
        if yardline + gained >= 100:
            result = "touchdown"
        elif yardline + gained <= 0:
            result = "safety"

    return gained, event, result


if __name__ == "__main__":
    print(
        SimulatePlay("ShortPass", "Base", 20)
    )
