from django.core.management.base import BaseCommand
from main.models import *


class Command(BaseCommand):
    help = "this is a test command"

    def handle(self, *args, **options):
        print("printing to console")
        self.stdout.write("printing to stdout")