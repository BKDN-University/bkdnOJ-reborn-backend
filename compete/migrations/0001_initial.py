# Generated by Django 4.0.4 on 2022-05-09 07:18

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
            ],
            options={
                'verbose_name': 'contest',
                'verbose_name_plural': 'contests',
                'ordering': [],
                'permissions': [('virtual_participate', 'Can virtual participate contests')],
            },
        ),
    ]
