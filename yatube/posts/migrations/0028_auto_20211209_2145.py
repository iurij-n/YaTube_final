# Generated by Django 2.2.16 on 2021-12-09 18:45

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0027_auto_20211209_0000'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_follow'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.CheckConstraint(check=models.Q(user__exact=django.db.models.expressions.F('author')), name='subscribe_to_yourself'),
        ),
    ]
