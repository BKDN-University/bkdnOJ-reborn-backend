# Generated by Django 4.0.4 on 2022-06-03 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compete', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestproblem',
            name='attempted_count',
            field=models.PositiveIntegerField(default=0, help_text='Number of users who has attempted this problem'),
        ),
        migrations.AddField(
            model_name='contestproblem',
            name='solved_count',
            field=models.PositiveIntegerField(default=0, help_text='Number of users who has solved this problem'),
        ),
    ]
