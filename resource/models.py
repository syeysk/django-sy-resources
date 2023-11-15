from django.db import models


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
        verbose_name='Фабрика-изготовитель',
        related_name='resource_made'
    )
