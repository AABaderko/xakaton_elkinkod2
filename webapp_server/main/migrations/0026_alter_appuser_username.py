# Generated by Django 5.1.6 on 2025-03-02 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_alter_appuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='username',
            field=models.CharField(blank=True, default='VlcZRE4OFLvpHaXA5G1D', max_length=50, null=True, unique=True),
        ),
    ]
