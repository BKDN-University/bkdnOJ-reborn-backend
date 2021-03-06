# Generated by Django 4.0.4 on 2022-05-30 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userprofile', '0001_initial'),
        ('submission', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.userprofile', verbose_name='user_profile'),
        ),
        migrations.AlterUniqueTogether(
            name='submissiontestcase',
            unique_together={('submission', 'case')},
        ),
    ]
