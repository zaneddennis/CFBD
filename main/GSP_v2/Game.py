from random import *

from main.models import *


class Game:

    # takes two Team objects
    def __init__(self, a, h):
        self.away = a
        self.home = h
        self.aAbb = a.school.abbreviation
        self.hAbb = h.school.abbreviation
        self.drives = []
        self.plays = []

    def simulate(self):
        scores = {
            self.aAbb: randint(3, 42),
            self.hAbb: randint(3, 42)
        }

        return GameResult(self.away, self.home, scores)


class GameResult:

    def __init__(self, a, h, score):
        self.away = a
        self.home = h
        self.homePoints = score[h.school.abbreviation]
        self.awayPoints = score[a.school.abbreviation]
        #self.drives = drives
        #self.plays = plays

    def __str__(self):
        return "GameResult<{} {} - {} {}>".format(self.home, self.homePoints, self.awayPoints, self.away)
