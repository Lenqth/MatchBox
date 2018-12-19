from django.contrib import admin

# Register your models here.
from .games.jong.models import GameJongResult
admin.site.register(GameJongResult)
