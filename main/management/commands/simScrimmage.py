from django.core.management.base import BaseCommand
from main.models import *
from main.GSP_v2 import Game as gs


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("away", type=str)
        parser.add_argument("home", type=str)

    def handle(self, *args, **options):
        print("{} @ {}".format(options["away"], options["home"]))

        a = Team.objects.get(school__abbreviation=options["away"], season__year=2020)
        h = Team.objects.get(school__abbreviation=options["home"], season__year=2020)
        game = gs.Game(a, h)
        gr = game.simulate()

        print(gr)
