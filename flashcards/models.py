from django.db import models
from django.contrib.auth.models import User


class FlashCard(models.Model):
    front = models.CharField('Słowo', max_length=120)
    back = models.CharField('Tłumaczenie', max_length=120)
    mnemo = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return self.front



