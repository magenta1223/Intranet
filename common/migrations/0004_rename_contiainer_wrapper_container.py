# Generated by Django 3.2.11 on 2022-02-23 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_wrapper_contiainer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wrapper',
            old_name='contiainer',
            new_name='container',
        ),
    ]
