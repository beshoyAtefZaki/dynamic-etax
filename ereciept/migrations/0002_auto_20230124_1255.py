# Generated by Django 3.2.5 on 2023-01-24 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ereciept', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='api_key',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='api_secret',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
