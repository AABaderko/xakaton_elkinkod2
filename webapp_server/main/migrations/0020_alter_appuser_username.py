# Generated by Django 5.1.6 on 2025-03-02 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_appuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='username',
            field=models.CharField(blank=True, default='1Idz3gPMr24fOGc9mkhD', max_length=50, null=True, unique=True),
        ),
    ]
