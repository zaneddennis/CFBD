import pandas as pd

from main.models import *
from .Play import *
from .util import *


drCols = ["Offense", "Result", "Start", "PlayCount", "Yards", "HalfOver", "GameOver"]
prCols = ["Yardline", "Gained", "Result", "Turnover", "Elapsed", "RunningClock"]

points = {
    "TOUCHDOWN": 7
}


class Game:

    # takes two Team objects
    def __init__(self, a, h):
        self.away = a
        self.home = h
        self.aAbb = a.school.abbreviation
        self.hAbb = h.school.abbreviation

        self.drives = []
        self.plays = []

        self.quarter = 1
        self.clock = timedelta(minutes=15, seconds=0)
        self.running = False

        self.down = 1
        self.dist = 10
        self.yardline = 25

    def simulate(self):
        scores = {
            self.aAbb: 0,
            self.hAbb: 0
        }

        # coin toss
        if randint(0, 1):
            off = self.aAbb
        else:
            off = self.hAbb

        # loop drives until game is over
        ko = True
        while True:
            dr = self.simDrive(off, self.yardline, kickoff=ko)

            # keep score
            res = dr[drCols.index("Result")]
            if res in points:
                scores[off] += points[res]

            self.drives.append(dr + (scores[self.aAbb], scores[self.hAbb]))

            if dr[drCols.index("GameOver")]:
                break

            # set up next drive:

            # swap offense
            if off == self.aAbb:
                off = self.hAbb
            else:
                off = self.aAbb

            # decide kickoff
            if res in ("TOUCHDOWN", "FGM"):
                ko = True
            else:
                ko = False
                self.yardline = 100 - self.yardline

        self.plays = pd.DataFrame(self.plays, columns=["Quarter", "Clock", "Down", "Dist"]+prCols)
        self.drives = pd.DataFrame(self.drives, columns=drCols+["AwayScore", "HomeScore"]).drop(columns=["HalfOver", "GameOver"])

        print(self.plays)
        print(self.drives)
        return GameResult(self.away, self.home, scores)

    def simDrive(self, off, ds, kickoff=False):
        self.down = 1
        self.dist = 10

        if kickoff:
            print("Kickoff")
            # sim kickoff
            if random() < 0.5:
                ds = 25
            else:
                ds = randint(15, 40)
            self.yardline = ds
            self.elapseClock(timedelta(seconds=randint(0, 10)))
        else:
            print("No kickoff")

        pc = 0
        dy = 0
        while True:
            # elapse play clock
            if self.running:
                if self.elapseClock(timedelta(seconds=randint(10, 25))):
                    if self.quarter == 3:  # halftime
                        return off, "HALFTIME", ds, pc, dy, True, False
                    elif self.quarter == 5:  # end of regulation
                        return off, "END OF REGULATION", ds, pc, dy, False, True

            # run play
            p = Play(self.yardline)
            pr = p.run()
            self.plays.append([self.quarter, str(self.clock), self.down, self.dist] + pr)
            pc += 1

            # elapse clock (play time)
            if self.elapseClock(pr[prCols.index("Elapsed")]):
                if self.quarter == 3:
                    return off, "HALFTIME", ds, pc, dy, True, False
                elif self.quarter == 5:
                    return off, "END OF REGULATION", ds, pc, dy, False, True

            # update game status variables
            self.running = pr[prCols.index("RunningClock")]

            self.dist -= pr[prCols.index("Gained")]
            self.yardline += pr[prCols.index("Gained")]
            dy += pr[prCols.index("Gained")]

            res = pr[prCols.index("Result")]
            if res == "TOUCHDOWN":
                return off, "TOUCHDOWN", ds, pc, dy, False, False
            elif res == "SAFETY":
                return  off, "SAFETY", ds, pc, dy, False, False

            if self.dist <= 0:
                self.down = 1
                self.dist = 10
            else:
                self.down += 1
                if self.down > 4:
                    return off, "TURNOVER ON DOWNS", ds, pc, dy, False, False

    def elapseClock(self, delta):
        self.clock = self.clock - delta
        if self.clock.days < 0:
            self.clock = timedelta(minutes=15, seconds=0)
            self.quarter += 1

            if self.quarter in (3, 5):  # return whether or not to conclude a drive
                return True
        return False


class GameResult:

    def __init__(self, a, h, score):
        self.away = a
        self.home = h
        self.homePoints = score[h.school.abbreviation]
        self.awayPoints = score[a.school.abbreviation]
        #self.drives = drives
        #self.plays = plays

    def __str__(self):
        return "GameResult<{} {} - {} {}>".format(self.away, self.awayPoints, self.homePoints, self.home)
