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
    STATUS_CHOICE_TO_ORDER = 5
    STATUS_CHOICE_PROVEN = 6
    STATUS_CHOICES = (
        (STATUS_CHOICE_OTHER, 'Другое'),
        (STATUS_CHOICE_REQUIRED, 'Запрашиваемый'),
        (STATUS_CHOICE_EXISTED, 'Наличный'),
        (STATUS_CHOICE_IN_MAKING, 'В процессе изготовления'),
        (STATUS_CHOICE_TO_ORDER, 'Под заказ'),
        (STATUS_CHOICE_PROVEN, 'Разведанный'),
    )
    UNIT_CHOICE_M = 1
    UNIT_CHOICE_KG = 2
    UNIT_CHOICE_OZ_T = 3
    UNIT_CHOICE_THINGS = 4
    UNIT_CHOICE_T = 5
    UNIT_CHOICE_MT = 6
    UNIT_CHOICES = (
        (UNIT_CHOICE_M, 'м'),
        (UNIT_CHOICE_KG, 'кг'),
        (UNIT_CHOICE_T, 'т'),
        (UNIT_CHOICE_MT, 'млн т'),
        (UNIT_CHOICE_OZ_T, 'тр. унц.'),
        (UNIT_CHOICE_THINGS, 'шт.'),
    )
    title = models.CharField('Название ресурса', max_length=240)
    status = models.IntegerField('Статус', choices=STATUS_CHOICES)
    count = models.FloatField('Количество')
    unit = models.IntegerField('Единица измерения', choices=UNIT_CHOICES) 
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


class ImageResource(models.Model):
    UPLOAD_TO = 'resource_images'
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Фотография ресурса', upload_to=UPLOAD_TO)
    is_main = models.BooleanField('Является ли фотография главной', null=True)


class ModelResource(models.Model):
    MODEL_TYPE_GCODE = 1
    MODEL_TYPE_PY_FREECAD = 2
    CHOICES_MODEL_TYPE = (
        ('G-code', MODEL_TYPE_GCODE),
        ('Python-макрос для FreeCAD', MODEL_TYPE_PY_FREECAD),
    )
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='models')
    model = models.FileField('Модель ресурса', upload_to='resource_models')
    model_type = models.IntegerField('Тип модели', choices=CHOICES_MODEL_TYPE)
