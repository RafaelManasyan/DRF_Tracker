from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from tracker.models import Habit
from tracker.paginators import HabitPagePagination
from tracker.permissions import IsCreator
from tracker.serializers import HabitSerializer


class MyHabitListAPIView(ListAPIView):
    pagination_class = HabitPagePagination
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(creator=self.request.user)


class PublicHabitListView(ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitCreateAPIView(CreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class HabitAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsCreator]
    queryset = Habit.objects.all()
