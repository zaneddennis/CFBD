from django.shortcuts import render
from django.views import generic
from main.models import *
from django.db.models import Max, Min
from main.forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse


# constants
SEASON = 2019
WEEK = 1


def index(request):
    countdownDays = 99

    context = {
        "countdownDays": countdownDays
    }

    return render(request, "index.html", context=context)


class SchoolDetailView(generic.DetailView):
    model = School


class CoachDetailView(generic.DetailView):
    model = Coach


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


def schedule(request):

    weekMax = Game.objects.filter(season=SEASON).aggregate(Max("week"))["week__max"]
    weekMin = Game.objects.filter(season=SEASON).aggregate(Min("week"))["week__min"]

    context = {
        "games": Game.objects.filter(season=SEASON),
        "range": range(weekMin, weekMax+1),
        "currentWeek": WEEK
    }

    return render(request, "schedule.html", context=context)
