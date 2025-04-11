from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from tracker.models import Habit
from tracker.paginators import HabitPagePagination
from tracker.permissions import IsCreator
from tracker.serializers import HabitSerializer


class MyHabitListAPIView(ListAPIView):
    """
    Список привычек пользователя.
    Возвращает пагинированный список привычек, созданных текущим пользователем.
    Требуется аутентификация.
    """
    pagination_class = HabitPagePagination
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(creator=self.request.user)


class PublicHabitListView(ListAPIView):
    """
    Список публичных привычек.
    Возвращает список привычек, отмеченных как публичные.
    Требуется аутентификация.
    """
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitCreateAPIView(CreateAPIView):
    """
    Создание новой привычки.
    Позволяет аутентифицированному пользователю создать новую привычку.
    При сохранении автоматически указывается создатель (creator).
    """
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class HabitAPIView(RetrieveUpdateDestroyAPIView):
    """
    Получение, обновление и удаление привычки.
    Позволяет владельцу (IsCreator) просматривать, изменять или удалять привычку.
    """
    serializer_class = HabitSerializer
    permission_classes = [IsCreator]
    queryset = Habit.objects.all()
