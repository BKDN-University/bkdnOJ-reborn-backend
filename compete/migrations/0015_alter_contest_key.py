# Generated by Django 4.0.4 on 2022-06-14 09:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compete', '0014_alter_contestparticipation_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='key',
            field=models.CharField(max_length=20, unique=True, validators=[django.core.validators.RegexValidator('^[a-z][a-z0-9]+$', 'Contest identifier must starts with a letter, contains only letters.'), django.core.validators.MinLengthValidator(4)], verbose_name='contest identifier'),
        ),
    ]