from django.db import models


class FlashCard(models.Model):
    front = models.CharField('Słowo', max_length=120)
    back = models.CharField('Tłumaczenie', max_length=120)
    mnemo = models.TextField(blank=True)

    def __str__(self):
        return self.front


class SiteUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField('Adres e-mail')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

