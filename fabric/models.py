from django.contrib.auth import get_user_model
from django.db import models


class Fabric(models.Model):
    title = models.CharField('Название фабрики', max_length=240)
    user = models.ForeignKey(get_user_model(), null=False, on_delete=models.CASCADE)
