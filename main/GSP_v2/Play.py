from datetime import *
from random import *


class Play:
    def __init__(self, yardline):
        self.yardline = yardline
        self.result = ""
        self.gained = 0
        self.turnover = False

        self.elapsed = timedelta(seconds=randint(3, 10))
        self.running = True  # if the clock is running after this play

    def run(self):
        self.gained = randint(-2, 10)

        if self.yardline + self.gained >= 100:
            self.gained = 100 - self.yardline
            self.result = "TOUCHDOWN"
        elif self.yardline + self.gained < 0:
            self.result = "SAFETY"

        return [self.yardline, self.gained, self.result, self.turnover, self.elapsed, self.running]
