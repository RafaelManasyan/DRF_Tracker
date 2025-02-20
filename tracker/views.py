from rest_framework.generics import ListAPIView

from tracker.models import Habit
from tracker.paginators import HabitPagePagination
from tracker.serializers import HabitSerializer


class HabitListAPIView(ListAPIView):
    queryset = Habit.objects.all()
    pagination_class = HabitPagePagination
    serializer_class = HabitSerializer

