from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.shortcuts import resolve_url

from django_sy_framework.linker.models import Linker


class Resource(models.Model):
    STATUS_CHOICE_OTHER = 1
    STATUS_CHOICE_REQUIRED = 2
    STATUS_CHOICE_EXISTED = 3
    STATUS_CHOICE_IN_MAKING = 4
    STATUS_CHOICES = (
        (STATUS_CHOICE_OTHER, 'Другое'),
        (STATUS_CHOICE_REQUIRED, 'Запрашиваемый'),
        (STATUS_CHOICE_EXISTED, 'Наличный'),
        (STATUS_CHOICE_IN_MAKING, 'В процессе изготовления'),
    )
    title = models.CharField('Название ресурса', max_length=240)
    status = models.IntegerField(choices=STATUS_CHOICES)
    fabric_maker = models.ForeignKey(
        'fabric.Fabric',
        on_delete=models.CASCADE,
        related_name='resource_made',
        null=True,
        verbose_name='Фабрика-изготовитель',
    )
    user_adder = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='resource_added',
        null=True,
        verbose_name='Пользователь, добавивший ресурс',
    )
    linker = GenericRelation(Linker, related_query_name='resource')

    @property
    def url(self):
        return '{}{}'.format(settings.SITE_URL, resolve_url('resource', self.pk))

    @property
    def url_new(self):
        return '{}{}'.format(settings.SITE_URL, resolve_url('resource_create'))
