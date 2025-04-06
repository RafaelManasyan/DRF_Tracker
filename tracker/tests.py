from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from tracker.models import Habit

User = get_user_model()


class HabitAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            creator=self.user,
            place="home",
            time="08:00:00",
            action="drink water",
            period=1,
            is_public=True
        )

    def test_my_habit_list(self):
        """Тест для MyHabitListAPIView"""
        url = reverse("tracker:habits")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data.get("results", [])) >= 1)

    def test_public_habit_list(self):
        """Тест для PublicHabitListView"""
        url = reverse("tracker:public-habits")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_habit(self):
        """Тест для HabitCreateAPIView"""
        url = reverse("tracker:create-habit")
        data = {
            "place": "office",
            "time": "09:00:00",
            "action": "read a book",
            "action_time": 100,
            "period": 1,
            "is_public": False
        }
        response = self.client.post(url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_habit_detail(self):
        """Тест для HabitAPIView (RetrieveUpdateDestroyAPIView)"""
        url = reverse("tracker:habit", kwargs={"pk": self.habit.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)