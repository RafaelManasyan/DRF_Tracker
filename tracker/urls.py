from django.urls import path

from tracker.views import (HabitAPIView, HabitCreateAPIView,
                           MyHabitListAPIView, PublicHabitListView)

app_name = "tracker"


urlpatterns = [
    path("habits/", MyHabitListAPIView.as_view(), name="habits"),
    path("public-habits/", PublicHabitListView.as_view(), name="public-habits"),
    path("create-habit/", HabitCreateAPIView.as_view(), name="create-habit"),
    path("habit/<int:pk>/", HabitAPIView.as_view(), name="habit"),
]
