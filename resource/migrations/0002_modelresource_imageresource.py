# Generated by Django 4.2.1 on 2024-01-06 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.FileField(upload_to='resource_models', verbose_name='Модель ресурса')),
                ('model_type', models.IntegerField(choices=[('G-code', 1), ('Python-макрос для FreeCAD', 2)], verbose_name='Тип модели')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models', to='resource.resource')),
            ],
        ),
        migrations.CreateModel(
            name='ImageResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='resource_images', verbose_name='Фотография ресурса')),
                ('is_main', models.BooleanField(null=True, verbose_name='Является ли фотография главной')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='resource.resource')),
            ],
        ),
    ]
