# Generated by Django 4.0.4 on 2022-05-09 07:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import helpers.fileupload


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('avatar', models.ImageField(default='avatar/default.png', upload_to=helpers.fileupload.PathAndRename('avatar/'))),
                ('global_ranking', models.BigIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
                'ordering': ['owner'],
                'permissions': (),
                'default_permissions': ('view', 'change'),
            },
        ),
    ]
