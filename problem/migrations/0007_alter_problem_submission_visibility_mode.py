# Generated by Django 4.0.4 on 2022-06-14 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0006_remove_problem_is_privated_to_orgs_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='submission_visibility_mode',
            field=models.CharField(choices=[('FOLLOW', "Follow bkdnOJ's setting."), ('ALWAYS', 'Users can see all submissions'), ('SOLVED', 'Users can see their own, and others if they have solved that problem'), ('ONLY_OWN', 'Users can only see their own submissions.'), ('HIDDEN', 'Submissions will never be visible.')], default='ONLY_OWN', help_text="Determine if users can view submissions for this problem. This is for public problems only. For problems within certain contests, please set the contest's own submission visibility setting.", max_length=16),
        ),
    ]
