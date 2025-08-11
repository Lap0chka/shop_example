from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower


class User(AbstractUser):
    email = models.EmailField()

    class Meta:
        constraints = [
            UniqueConstraint(Lower('email'), name='uniq_user_email_ci')
        ]
