import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20211025_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, default='empty', null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.Group'),
        ),
    ]
