from django.db import models


class Fabric(models.Model):
    title = models.CharField('Название фабрики', max_length=240)
