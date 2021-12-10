# Generated by Django 2.2.16 on 2021-12-09 20:14

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0032_auto_20211209_2313'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='subscribe_to_yourself',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='user',
            new_name='user_1',
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, user_1=django.db.models.expressions.F('author')), name='subscribe_to_yourself'),
        ),
    ]
