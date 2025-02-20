from django.urls import path

from tracker.views import HabitListAPIView

app_name = 'tracker'


urlpatterns = [
    path('habits/', HabitListAPIView.as_view(), name='habits')
]
