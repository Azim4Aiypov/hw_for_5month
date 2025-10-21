from django.contrib.auth.models import AbstractUser
from django.db import models
import random

class User(AbstractUser):
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)

    def generate_confirmation_code(self):
        code = f"{random.randint(0, 999999):06d}"
        self.confirmation_code = code
        self.is_active = False
        self.save()
        return code
