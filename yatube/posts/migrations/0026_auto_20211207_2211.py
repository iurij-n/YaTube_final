# Generated by Django 2.2.16 on 2021-12-07 19:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0025_auto_20211207_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='author',
            field=models.ForeignKey(help_text='Имя автора публикаций', on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='Автор записей'),
        ),
    ]
