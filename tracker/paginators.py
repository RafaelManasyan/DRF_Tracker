from rest_framework.pagination import PageNumberPagination


class HabitPagePagination(PageNumberPagination):
    page_size = 5
