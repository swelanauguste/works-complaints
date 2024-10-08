# Generated by Django 5.1.1 on 2024-09-22 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('technician', 'Technician'), ('assistant', 'Engineering Assistant'), ('engineer', 'Engineer'), ('chief engineer', 'Chief Engineer'), ('chief engineer secretary', 'Chief Engineer Secretary'), ('deputy chief engineer', 'Deputy Chief Engineer'), ('deputy chief engineer secretary', 'Deputy Chief Engineer Secretary')], default='technician', max_length=50),
        ),
    ]
