
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cfbd.settings")
import django
django.setup()

from main import models
import GSP.Game as GSP
import datetime


if __name__ == "__main__":
    toPlay = models.Game.objects.filter(datetime__lte=datetime.datetime.now()).filter(awayScore__isnull=True)

    #g = GSP.Game("TCU", "Baylor")
    #print(g.Simulate())
    #print()

    results = []
    for g in toPlay:
        r = GSP.Game(g.home, g.away).Simulate()
        results.append(r)
        g.awayScore = r.awayPoints
        g.homeScore = r.homePoints
        g.save()

    print()
    print()
    print()
    for i in range(len(toPlay)):
        print(toPlay[i])
        print(results[i])
        print()
