from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("school/<str:pk>", views.SchoolDetailView.as_view(), name="school-detail"),
    path("coach/<int:pk>", views.CoachDetailView.as_view(), name="coach-detail"),
    path("team/<int:pk>", views.TeamDetailView.as_view(), name="team-detail"),
    path("player/<int:pk>", views.PlayerDetailView.as_view(), name="player-detail"),
    path("messages", views.messages, name="messages"),
    path("schedule", views.schedule, name="schedule"),
    path("standings", views.standings, name="standings")
]