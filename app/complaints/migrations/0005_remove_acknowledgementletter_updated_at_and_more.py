# Generated by Django 5.1.1 on 2024-09-17 23:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0004_acknowledgementletter'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acknowledgementletter',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='acknowledgementletter',
            name='updated_by',
        ),
        migrations.AlterField(
            model_name='acknowledgementletter',
            name='complaint',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='letters', to='complaints.complaint'),
        ),
        migrations.CreateModel(
            name='AssignInvestigator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('complaint', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='complaints.complaint')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('investigator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='investigator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
