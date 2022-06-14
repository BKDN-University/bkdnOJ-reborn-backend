# Generated by Django 4.0.4 on 2022-06-05 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compete', '0004_alter_contestsubmission_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContestPartcipantBestSubmissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='best_submission', to='compete.contestparticipation', verbose_name='participant')),
                ('problem', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='best_submission', to='compete.contestproblem', verbose_name='problem')),
                ('submission', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='best_submission', to='compete.contestsubmission', verbose_name='submission')),
            ],
            options={
                'verbose_name': "participant's best submission",
                'verbose_name_plural': "participant's best submissions",
            },
        ),
    ]
