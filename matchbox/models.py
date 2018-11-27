from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class GameResult(models.Model):
        date = models.DateTimeField(auto_now_add=True, blank=True)
#        = models.ForeignKey(User)
