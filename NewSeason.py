
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cfbd.settings")
import django
django.setup()

from main import models
from django.db.models import Max


YEAR = 2020
if __name__ == "__main__":
    print("Initializing new Season...")

    maxYear = models.Season.objects.aggregate(Max("year"))["year__max"]
    assert YEAR != maxYear

    s = models.Season(YEAR)
    s.save()

    schools = models.School.objects.all()
    for school in schools:
        print(school)
        team = models.Team(school=school, coach=school.coach, season=s, wins=0, losses=0, conf_wins=0, conf_losses=0)
        team.save()
