# Generated by Django 5.1.1 on 2024-09-18 14:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0016_alter_zone_district'),
        ('users', '0004_zone_alter_user_options_user_zone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='zone',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.zone'),
        ),
        migrations.DeleteModel(
            name='Zone',
        ),
    ]
