# Generated by Django 5.1.1 on 2024-09-17 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0005_remove_acknowledgementletter_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='acknowledgementletter',
            options={'ordering': ['-created_at']},
        ),
    ]
