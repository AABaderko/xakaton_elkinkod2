# Generated by Django 5.1.6 on 2025-03-02 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_appuser_username'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messagechat',
            options={'ordering': ['-sended_at']},
        ),
        migrations.AlterField(
            model_name='appuser',
            name='username',
            field=models.CharField(blank=True, default='RVtqALerNHSx54BcuIO8', max_length=50, null=True, unique=True),
        ),
    ]
