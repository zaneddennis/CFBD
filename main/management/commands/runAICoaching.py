from django.core.management.base import BaseCommand
from main.models import *


def SetPositions(t):
    # standard positions are set by default

    # OL
    #print("Assigning OLs")
    olPlayers = t.playerteam_set.filter(player__position="OL")
    olPositions = ("LT", "RT", "C", "RG", "LG")
    o = 0
    for pt in olPlayers:
        p = pt.player
        p.position = olPositions[o]
        p.save()

        o += 1
        if o >= 5:
            o = 0

    # EDGE
    #print("Assigning EDGEs")
    edgePlayers = t.playerteam_set.filter(player__position="EDGE")
    for pt in edgePlayers:
        p = pt.player
        p.position = "DE"
        p.save()

    # S
    #print("Assigning Safeties")
    sPlayers = t.playerteam_set.filter(player__position="S")
    sPositions = ("FS", "SS")
    s = 0
    for pt in sPlayers:
        p = pt.player
        p.position = sPositions[s]
        p.save()

        s += 1
        if s >= 2:
            s = 0


def SetStrings(t):
    for pos in ["QB", "RB", "WR", "TE", "LT", "LG", "C", "RG", "RT",
                 "DT", "DE", "LB", "CB", "FS", "SS", "K", "P"]:
        #print("Setting depth chart for {}s".format(pos))

        ptList = t.playerteam_set.filter(player__position=pos).order_by("player__stars")
        if len(ptList) < 2:
            print("WARNING: NOT ENOUGH {}s".format(pos))

        s = 1
        for pt in ptList:
            pt.string = s
            s += 1
            pt.save()


def CoachTeam(c, pos=True, strings=True):
    print(c)

    t = c.school.team_set.order_by("season__year").last()
    print(t)

    if pos:  # set positions (at beginning of season)
        SetPositions(t)

    if str:  # set strings (every week)
        SetStrings(t)

    print()


class Command(BaseCommand):
    help = "this is a test command"

    def handle(self, *args, **options):
        self.stdout.write("Running weekly coaching for AI coaches...")

        for c in Coach.objects.all():
            if c.ai:
                CoachTeam(c)
