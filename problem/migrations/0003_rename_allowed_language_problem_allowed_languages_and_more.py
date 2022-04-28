# Generated by Django 4.0.3 on 2022-04-28 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_initial'),
        ('problem', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='allowed_language',
            new_name='allowed_languages',
        ),
        migrations.RemoveField(
            model_name='problem',
            name='shared_orgs',
        ),
        migrations.AddField(
            model_name='problem',
            name='organizations',
            field=models.ManyToManyField(blank=True, default=[], to='organization.organization'),
        ),
        migrations.AddField(
            model_name='problem',
            name='published_at',
            field=models.DateTimeField(null=True),
        ),
    ]
