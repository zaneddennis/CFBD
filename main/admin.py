from django.contrib import admin
from main.models import *


class TeamAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)


class PlayerAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)


class GameAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)


admin.site.register(Season)
admin.site.register(Conference)
admin.site.register(School)
admin.site.register(Coach)
admin.site.register(AI)
admin.site.register(Message)
admin.site.register(Game, GameAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerTeam)
admin.site.register(Formation)
admin.site.register(DefensiveFormation)
