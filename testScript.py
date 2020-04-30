
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

        if g.awayScore > g.homeScore:
            winner = g.away
            loser = g.home
        else:
            winner = g.home
            loser = g.away

        winner.wins += 1
        loser.losses += 1

        if g.home.school.conference == g.away.school.conference:
            winner.conf_wins += 1
            loser.conf_losses += 1

        winner.save()
        loser.save()

    print()
    print()
    print()
    for i in range(len(toPlay)):
        print(toPlay[i])
        print(results[i])
        print()
