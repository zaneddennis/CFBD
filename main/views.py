from django.shortcuts import render
from django.views import generic
from main.models import *
from django.db.models import F, Max, Min, Count
from main.forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse

from .Subtemplating import standings as stGenerator
from .Subtemplating import depthChart as dcGenerator
from .GSP_v2 import Game as GameSimulation


# constants
SEASON = 2020
WEEK = 0

COACHESPOLL = [
    "LSU", "Ohio State", "Clemson", "Georgia", "Alabama", "Oregon", "Utah", "Minnesota", "Penn State", "Oklahoma", "Florida", "Auburn", "Baylor", "Wisconsin", "Michigan", "Texas", "Iowa", "Oklahoma State", "Kansas State"
]


def index(request):
    countdownDays = 99

    context = {
        "countdownDays": countdownDays
    }

    return render(request, "index.html", context=context)


# Detail views

class SchoolDetailView(generic.DetailView):
    model = School


class CoachDetailView(generic.DetailView):
    model = Coach


class TeamDetailView(generic.DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        context["schedule"] = Game.objects.filter(away__school=context["team"].school) | Game.objects.filter(home__school=context["team"].school)
        context["schedule"] = context["schedule"].order_by("week")
        return context


class PlayerDetailView(generic.DetailView):
    model = Player


class GameDetailView(generic.DetailView):
    model = Game

    def post(self, request, *args, **kwargs):
        g = Game.objects.get(id=kwargs["pk"])

        if g.isScrimmage and g.status == "F":

            gSim = GameSimulation.Game(g.away, g.home)
            results = gSim.simulate()

            g.status = "C"
            g.awayScore = results.awayPoints
            g.homeScore = results.homePoints

            g.save()

        context = {
            "game": g
        }

        return render(request, "main/game_detail.html", context=context)


# NavBar Views

def schedule(request):

    weekMax = Game.objects.filter(season=SEASON).aggregate(Max("week"))["week__max"]
    weekMin = Game.objects.filter(season=SEASON).aggregate(Min("week"))["week__min"]

    context = {
        "games": Game.objects.filter(season=SEASON),
        "range": range(weekMin, weekMax+1),
        "currentWeek": WEEK
    }
    print(context["games"])

    return render(request, "schedule.html", context=context)


def standings(request):

    conferences = Conference.objects.all()

    context = {
        "CP": [Team.objects.get(school__name=s, season__year=SEASON) for s in COACHESPOLL],
        "conferences": [stGenerator.GenerateStandingsHTML(Conference.objects.get(abbreviation=c.abbreviation), Team.objects.filter(school__conference__abbreviation=c.abbreviation, season__year=SEASON)) for c in conferences]
    }

    return render(request, "standings.html", context=context)


def coaching(request):
    uc = Coach.objects.filter(user=request.user)
    if uc.exists():
        uc = uc.first()
    else:
        uc = None

    context = {"userCoach": uc}

    return render(request, "coaching.html", context=context)


def messages(request):
    sent = Message.objects.filter(sender=request.user)
    received = Message.objects.filter(recipient=request.user)
    conversations = {}

    for m in sent:
        if m.recipient.username not in conversations:
            conversations[m.recipient.username] = []
        conversations[m.recipient.username].append(m)
    for m in received:
        if m.sender.username not in conversations:
            conversations[m.sender.username] = []
        conversations[m.sender.username].append(m)

    for other in conversations:
        conversations[other].sort(key=lambda m: m.sentTime)

    if request.method == "POST":
        form = SendMessageForm(request.POST)

        if form.is_valid():
            recipient = User.objects.get(username=form.cleaned_data["recipient"])

            m = Message(sender=request.user, recipient=recipient, content=form.cleaned_data["content"])
            m.save()

            return HttpResponseRedirect(reverse("messages"))

    else:
        form = SendMessageForm()

    context = {
        "messageList": Message.objects.filter(recipient=request.user) | Message.objects.filter(sender=request.user),
        "conversations": conversations,
        "form": form
    }
    return render(request, "messages.html", context=context)


# Coaching Subsections

def depthChart(request):
    if request.POST:
        print("SAVE STRING CHANGES TO DB")
        dcGenerator.SaveChanges(request.POST)

    uc = Coach.objects.filter(user=request.user).first()
    team = uc.school.team_set.last()

    positions = ["QB", "RB", "WR", "TE", "LT", "LG", "C", "RG", "RT",
                 "DT", "DE", "LB", "CB", "FS", "SS", "K", "P"]  # todo: vary position list by scheme

    posDict = {}
    for pos in positions:
        posDict[pos] = dcGenerator.GeneratePositionTable(pos, team, positions)

    context = {
        "team": team,
        "posDict": posDict
    }

    return render(request, "depthChart.html", context=context)


# Other Miscellaneous Pages

def scrimmage(request):
    if request.method == "POST":
        form = ScrimmageSetupForm(request.POST)
        if form.is_valid():
            # create new Game
            a = Team.objects.get(school__abbreviation=request.POST["away"])
            h = Team.objects.get(school__abbreviation=request.POST["home"])
            game = Game(away=a, home=h, isScrimmage=True)
            game.save()

            return HttpResponseRedirect(reverse("game-detail", args=[game.id]))

    else:
        form = ScrimmageSetupForm()

    context = {
        "form": form
    }

    return render(request, "scrimmage.html", context=context)
