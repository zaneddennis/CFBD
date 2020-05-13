from django.core.management.base import BaseCommand
from main.models import *


class Command(BaseCommand):
    help = "this is a test command"

    def handle(self, *args, **options):
        self.stdout.write("Wiping all Scrimmage games from the database...")

        toWipe = Game.objects.filter(isScrimmage=True)
        for g in toWipe:
            g.delete()