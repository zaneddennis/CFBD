
import pandas as pd
from random import *
from . import Play


# returns (points, yardline)
def SimulateDrive(startYard, off):
    assert startYard >= 0
    print("BEGIN DRIVE: {}".format(off))
    drive = {
        "Offense": off,
        "Start": startYard,
        "End": 0,
        "Event": "",
        "Result": "",
        "Points": 0
    }
    plays = []

    yardline = startYard
    down = 1
    dist = 10

    while down < 5:
        # call play
        playcall = CallPlayAI(down, dist, yardline)
        defcall = CallDefAI(down, dist, yardline)

        play = {
            "Time": 0,
            "Down": down,
            "Dist": dist,
            "Yardline": yardline,
            "Playcall": playcall,
            "Defcall": defcall,
            "Gained": 0,
            "Event": "",
            "Result": ""
        }

        # simulate play
        print(down, "&", dist, "-", yardline)
        gained, event, result = Play.SimulatePlay(playcall, defcall, yardline)
        play["Gained"] = gained
        play["Event"] = event
        play["Result"] = result
        print()
        yardline += gained

        if result in ["interception", "fumble"]:
            print("TURNOVER")
            print()

            if yardline >= 100:
                drive["End"] = 80
            else:
                drive["End"] = yardline
            break

        elif result == "touchdown":
            print(result.upper())
            print()
            drive["End"] = None
            drive["Points"] = 7
            break

        elif result == "FGM":
            print(result)
            print()
            drive["End"] = None
            drive["Points"] = 3
            break

        elif result == "missed FG":
            drive["End"] = yardline
            break

        elif result == "punt":
            if yardline >= 100:
                yardline = 80
            drive["End"] = yardline
            break

        elif gained >= dist:
            down = 1
            dist = 10

            if yardline > 90:
                dist = 100 - yardline

            print("1st Down")
            print()

        else:
            down += 1
            dist -= gained

        plays.append(play)
    plays.append(play)

    drive["Result"] = result

    if down == 5:
        drive["End"] = yardline
        drive["Result"] = "downs"

    plays = pd.DataFrame(plays)
    return drive, plays


def CallPlayAI(down, dist, yardline):
    if down == 4 and dist > 2:
        if yardline >= 70:
            return "FGA"
        else:
            return "Punt"
    else:
        if down >= 3 and dist <= 3:
            return choices(["Run", "ShortPass"], [0.7, 0.3])[0]

        elif down >= 3 and dist >= 5:
            return choices(["Run", "ShortPass", "Pass", "DeepPass"], [0.1, 0.1, 0.4, 0.4])[0]

        return choices(["Run", "ShortPass", "Pass", "DeepPass"])[0]


def CallDefAI(down, dist, yardline):
    if down >= 3 and dist <= 3:
        return "Base"

    elif down >= 3 and dist >= 5:
        return choices(["Base", "Nickel", "Dime", "Blitz"], [0.1, 0.3, 0.2, 0.2])[0]

    else:
        return choices(["Base", "Nickel", "Dime", "Blitz"])[0]


class Game:

    def __init__(self, h, a):
        self.home = h
        self.away = a
        self.drives = []
        self.plays = pd.DataFrame(columns=["Time", "Down", "Dist", "Yardline", "Playcall", "Defcall", "Gained", "Result"])

    def Simulate(self):
        #hScore = 0
        #aScore = 0
        score = {
            self.home: 0,
            self.away: 0
        }
        yardline = 20

        PACE = 10  # drives per game

        for i in range(0, PACE*2, 2):
            j = 0
            for t in (self.away, self.home):
                drive, drivePlays = SimulateDrive(yardline, t)
                print(drive)
                print()
                score[t] += drive["Points"]

                if drive["End"]:  # no score
                    yardline = 100 - drive["End"]
                else:
                    yardline = 20

                drivePlays.loc[:, "Time"] = i + j

                self.drives.append(drive)
                self.plays = self.plays.append(drivePlays, sort=False)
                j += 1

        if score[self.home] == score[self.away]:
            print("OVERTIME")
            print()

            if randint(0, 1):
                score[self.home] += 6
                score[self.away] += 3
            else:
                score[self.home] += 3
                score[self.away] += 6

        self.plays = self.plays.reset_index(drop=True)
        self.plays = self.plays[["Time", "Down", "Dist", "Yardline", "Playcall", "Defcall", "Gained", "Event", "Result"]]

        self.drives = pd.DataFrame(self.drives)
        self.drives = self.drives[["Offense", "Start", "End", "Result", "Points"]]
        print(self.plays)
        print(self.drives)
        return GameResult(self.home, self.away, score, self.drives, self.plays)


class GameResult:

    def __init__(self, h, a, score, drives, plays):
        self.home = h
        self.away = a
        self.homePoints = score[h]
        self.awayPoints = score[a]
        self.drives = drives
        self.plays = plays

    def __str__(self):
        return "GameResult<{} {} - {} {}>".format(self.home, self.homePoints, self.awayPoints, self.away)
