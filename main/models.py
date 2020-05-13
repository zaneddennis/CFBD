from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Avg

import numpy as np


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
            #print(self.school)
            #print(type(self.school))
            #print()
            try:
                return "Coach<" + str(self.ai) + ", " + self.school.name + ">"  # weird bug in this line when I try to do school.name???
            except:
                return"Coach<" + str(self.ai) + ", ERROR_NO_SCHOOL>"
            #return "Coach<" + str(self.ai) + ">"

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

    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True)
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True)

    wins = models.IntegerField()
    losses = models.IntegerField()
    conf_wins = models.IntegerField()
    conf_losses = models.IntegerField()

    def __str__(self):
        try:
            return "Team<{}, {}>".format(self.school.name, self.season.year)
        except:
            return "Team<ERROR>"

    def TalentRatings(self):
        offPos = ("QB", "RB", "WR", "TE", "OL", "LT", "LG", "C", "RG", "RT")
        defPos = ("DT", "DE", "EDGE", "LB", "S", "FS", "SS", "CB")
        stPos = ("K", "P")

        result = {
            "OFF": self.playerteam_set.filter(player__position__in=offPos).aggregate(Avg("player__stars"))["player__stars__avg"],
            "DEF": self.playerteam_set.filter(player__position__in=defPos).aggregate(Avg("player__stars"))["player__stars__avg"],
            "ST": self.playerteam_set.filter(player__position__in=stPos).aggregate(Avg("player__stars"))["player__stars__avg"],
        }

        return result


class Game(models.Model):

    STATUS_CHOICES = (
        ("F", "Future"),
        ("P", "In Progress"),
        ("C", "Complete"),
    )

    # for all games
    away = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name="+")
    home = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name="+")
    datetime = models.DateTimeField(blank=True, null=True)
    season = models.IntegerField(blank=True, null=True)
    week = models.IntegerField(blank=True, null=True)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="F")
    isScrimmage = models.BooleanField(default=False)

    # for past games
    awayScore = models.IntegerField(blank=True, null=True)
    homeScore = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Game<{} @ {}, {}, W{}>".format(self.away, self.home, self.season, self.week)


class Player(models.Model):

    AGE_CHOICES = (
        ("FR", "Freshman"),
        ("SO", "Sophomore"),
        ("JR", "Junior"),
        ("SR", "Senior"),
        ("AL", "Alum")
    )

    POS_CHOICES = (
        ("QB", "Quarterback"),
        ("RB", "Running Back"),
        ("WR", "Wide Receiver"),
        ("TE", "Tight End"),
        ("OL", "Offensive Line"),
        ("DT", "Defensive Tackle"),
        ("EDGE", "Edge Defender"),
        ("LB", "Linebacker"),
        ("CB", "Cornerback"),
        ("S", "Safety"),
        ("K", "Kicker"),
        ("P", "Punter")
    )

    first = models.CharField(max_length=20)
    last = models.CharField(max_length=20)
    jersey = models.IntegerField(default=1)
    height = models.IntegerField()
    weight = models.IntegerField()

    position = models.CharField(max_length=2, choices=POS_CHOICES)
    age = models.CharField(max_length=2, choices=AGE_CHOICES)
    scholarship = models.BooleanField()
    stars = models.IntegerField(default=2)

    t_strength = models.FloatField(default=0.0)
    t_athleticism = models.FloatField(default=0.0)
    t_dexterity = models.FloatField(default=0.0)
    t_iq = models.FloatField(default=0.0)
    t_personality = models.FloatField(default=0.0)
    t_arm = models.FloatField(default=0.0)
    t_leg = models.FloatField(default=0.0)

    s_armStr = models.FloatField(default=0.0)
    s_armAccShort = models.FloatField(default=0.0)
    s_armAccMed = models.FloatField(default=0.0)
    s_armAccLong = models.FloatField(default=0.0)

    s_readDefPass = models.FloatField(default=0.0)
    s_readDefRun = models.FloatField(default=0.0)

    s_speed = models.FloatField(default=0.0)
    s_acceleration = models.FloatField(default=0.0)
    s_agility = models.FloatField(default=0.0)
    s_runPower = models.FloatField(default=0.0)
    s_vertical = models.FloatField(default=0.0)
    s_hands = models.FloatField(default=0.0)

    s_runBlock = models.FloatField(default=0.0)
    s_passBlock = models.FloatField(default=0.0)

    s_tackApproach = models.FloatField(default=0.0)
    s_tackBringDown = models.FloatField(default=0.0)
    s_shedBlockStr = models.FloatField(default=0.0)
    s_shedBlockAgl = models.FloatField(default=0.0)
    s_coverMan = models.FloatField(default=0.0)
    s_coverZone = models.FloatField(default=0.0)
    s_readOff = models.FloatField(default=0.0)

    s_kickPow = models.FloatField(default=0.0)
    s_kickAcc = models.FloatField(default=0.0)
    s_puntPow = models.FloatField(default=0.0)
    s_puntAcc = models.FloatField(default=0.0)

    def __str__(self):
        return "Player<{} {}>".format(self.first, self.last)

    def GetBadges(self):
        bl = []

        if self.s_armStr > 85:
            bl.append("CAN III")
        elif self.s_armStr > 75:
            bl.append("CAN II")
        elif self.s_armStr > 65:
            bl.append("CAN I")

        ttn = np.mean((self.s_armAccShort, self.s_armAccMed, self.s_armAccLong))
        if ttn > 75:
            bl.append("TTN III")
        elif ttn > 65:
            bl.append("TTN II")
        elif ttn > 60:
            bl.append("TTN I")

        if self.s_readDefPass > 85:
            bl.append("ASE III")
        elif self.s_readDefPass > 75:
            bl.append("ASE II")
        elif self.s_readDefPass > 65:
            bl.append("ASE I")

        if self.s_readDefRun > 85:
            bl.append("TSA III")
        elif self.s_readDefRun > 75:
            bl.append("TSA II")
        elif self.s_readDefRun > 65:
            bl.append("TSA I")

        blz = np.mean((self.s_speed, self.s_acceleration))
        if blz > 80:
            bl.append("BLZ III")
        elif blz > 70:
            bl.append("BLZ II")
        elif blz > 65:
            bl.append("BLZ I")

        if self.s_agility > 85:
            bl.append("OAD III")
        elif self.s_agility > 75:
            bl.append("OAD II")
        elif self.s_agility > 65:
            bl.append("OAD I")

        if self.s_runPower > 85:
            bl.append("TRK III")
        elif self.s_runPower > 75:
            bl.append("TRK II")
        elif self.s_runPower > 65:
            bl.append("TRK I")

        if self.s_vertical > 85:
            bl.append("SKY III")
        elif self.s_vertical > 75:
            bl.append("SKY II")
        elif self.s_vertical > 65:
            bl.append("SKY I")

        if self.s_hands > 85:
            bl.append("STK III")
        elif self.s_hands > 75:
            bl.append("STK II")
        elif self.s_hands > 65:
            bl.append("STK I")

        if self.s_runBlock > 85:
            bl.append("DOZ III")
        elif self.s_runBlock > 75:
            bl.append("DOZ II")
        elif self.s_runBlock > 65:
            bl.append("DOZ I")

        if self.s_passBlock > 85:
            bl.append("BWK III")
        elif self.s_passBlock > 75:
            bl.append("BWK II")
        elif self.s_passBlock > 65:
            bl.append("BWK I")

        ham = np.mean((self.s_tackApproach, self.s_tackBringDown))
        if ham > 80:
            bl.append("HAM III")
        elif ham > 70:
            bl.append("HAM II")
        elif ham > 65:
            bl.append("HAM I")

        unb = np.mean((self.s_shedBlockAgl, self.s_shedBlockStr))
        if unb > 80:
            bl.append("UNB III")
        elif unb > 70:
            bl.append("UNB II")
        elif unb > 65:
            bl.append("UNB I")

        if self.s_readOff > 85:
            bl.append("DET III")
        elif self.s_readOff > 75:
            bl.append("DET II")
        elif self.s_readOff > 65:
            bl.append("DET I")

        lck = np.mean((self.s_coverMan, self.s_coverZone))
        if lck > 80:
            bl.append("LCK III")
        elif lck > 70:
            bl.append("LCK II")
        elif lck > 65:
            bl.append("LCK I")

        return ", ".join(bl)


class PlayerTeam(models.Model):

    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    age = models.CharField(max_length=2, choices=Player.AGE_CHOICES)
    string = models.IntegerField(default=99)

    # on-field (box score) stats go here
