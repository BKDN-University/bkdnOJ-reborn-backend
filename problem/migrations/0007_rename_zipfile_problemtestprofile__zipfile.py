# Generated by Django 4.0.3 on 2022-05-02 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0006_alter_testcase_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problemtestprofile',
            old_name='zipfile',
            new_name='_zipfile',
        ),
    ]