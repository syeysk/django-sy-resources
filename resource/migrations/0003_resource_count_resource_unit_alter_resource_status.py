# Generated by Django 4.2.1 on 2025-01-05 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0002_modelresource_imageresource'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='count',
            field=models.PositiveIntegerField(default=1, verbose_name='Количество'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resource',
            name='unit',
            field=models.IntegerField(choices=[(1, 'м'), (2, 'кг'), (3, 'тр. унция'), (4, 'шт.')], default=4, verbose_name='Единица измерения'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='resource',
            name='status',
            field=models.IntegerField(choices=[(1, 'Другое'), (2, 'Запрашиваемый'), (3, 'Наличный'), (4, 'В процессе изготовления'), (5, 'Под заказ'), (6, 'Разведанный')], verbose_name='Статус'),
        ),
    ]
