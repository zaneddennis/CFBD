from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Season(models.Model):

    year = models.IntegerField(primary_key=True)
    champion = models.ForeignKey("School", on_delete=models.SET_NULL, null=True, related_name="+", blank=True)


class Conference(models.Model):

    name = models.CharField(max_length=40)
    abbreviation = models.CharField(max_length=4)
    division1 = models.CharField(max_length=10, blank=True)
    division2 = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.abbreviation


class School(models.Model):

    name = models.CharField(max_length=40)
    mascot = models.CharField(max_length=40)
    abbreviation = models.CharField(max_length=4, primary_key=True)
    location = models.CharField(max_length=40)
    state = models.CharField(max_length=2)

    conference = models.ForeignKey(Conference, on_delete=models.SET_NULL, null=True)
    division = models.CharField(max_length=10, blank=True)

    coach = models.ForeignKey("Coach", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")

    def get_absolute_url(self):
        return reverse("school-detail", args=[str(self.id)])

    def __str__(self):
        return self.name + " " + self.mascot + " [{}]".format(self.abbreviation)


class AI(models.Model):

    name = models.CharField(max_length=30)

    def __str__(self):
        return "AI<{}>".format(self.name)


class Coach(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ai = models.ForeignKey(AI, on_delete=models.SET_NULL, null=True, blank=True)
    almaMater = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, related_name="+")
    school = models.OneToOneField(School, on_delete=models.SET_NULL, null=True, related_name="+")

    def __str__(self):
        if self.user:
            return "Coach<" + self.user.username + ", " + self.school.name + ">"
        else:
            return "Coach<" + str(self.ai) + ", " + self.school.name + ">"

    @property
    def get_name(self):
        if self.user:
            return self.user.username
        elif self.ai:
            return self.ai.name


class Message(models.Model):

    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="+")
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="+")
    content = models.CharField(max_length=400)

    sentTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Message<{}, {}, \"{}{}\">".format(self.sender, self.recipient, self.content[:20], "..." if len(self.content) > 10 else "")


class Team(models.Model):

    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True)
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True)

    wins = models.IntegerField()
    losses = models.IntegerField()
    conf_wins = models.IntegerField()
    conf_losses = models.IntegerField()

    def __str__(self):
        return "Team<{}, {}>".format(self.school.name, self.season.year)


class Game(models.Model):

    # for all games
    away = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name="+")
    home = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name="+")
    datetime = models.DateTimeField()
    season = models.IntegerField()
    week = models.IntegerField()

    # for past games
    awayScore = models.IntegerField(blank=True, null=True)
    homeScore = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Game<{} @ {}, {}, W{}>".format(self.away, self.home, self.season, self.week)
