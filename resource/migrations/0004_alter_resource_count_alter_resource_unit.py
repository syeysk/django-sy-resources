# Generated by Django 4.2.1 on 2025-01-05 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0003_resource_count_resource_unit_alter_resource_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='count',
            field=models.FloatField(verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='unit',
            field=models.IntegerField(choices=[(1, 'м'), (2, 'кг'), (5, 'т'), (6, 'млн т'), (3, 'тр. унц.'), (4, 'шт.')], verbose_name='Единица измерения'),
        ),
    ]
