# Generated by Django 5.1.5 on 2025-02-18 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0030_delete_category_alter_complaint_lat_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='location',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
