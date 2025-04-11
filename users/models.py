from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="E-mail")
    phone_number = models.CharField(
        max_length=15, unique=True, verbose_name="Номер телефона"
    )
    avatar = models.ImageField(blank=True, upload_to="media/", verbose_name="Аватар")
    tg_chat_id = models.CharField(
        max_length=9,
        verbose_name="ID пользователя в Телеграм",
        unique=True,
        blank=True,
        null=True,
    )
    notificator_is_on = models.BooleanField(default=True, verbose_name='Подключение уведомлений')

    REQUIRED_FIELDS = [
        "email",
    ]
