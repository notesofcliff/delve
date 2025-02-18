from enum import Enum
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(
        default=uuid4,
        primary_key=True,
    )


class ThemeEnum(models.TextChoices):
    darkly = ("darkly", "darkly")
    sandstone = ("sandstone", "sandstone")
    slate = ("slate", "slate")
    solar = ("solar", "solar")
    vapor = ("vapor", "vapor")
    sketchy = ("sketchy", "sketchy")

class ModeEnum(models.TextChoices):
    dark = ("dark", "dark")
    light = ("light", "light")

class UserProfile(models.Model):
    theme = models.CharField(
        max_length=255,
        default="slate",
        choices=ThemeEnum,
    )
    mode = models.CharField(
        max_length=255,
        default="dark",
        choices=ModeEnum,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    def background(self):
        return self.mode
    
    def foreground(self):
        return "light" if self.mode == "dark" else "dark"