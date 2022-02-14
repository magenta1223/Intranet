# Generated by Django 3.2.11 on 2022-02-09 14:35

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_auto_20220209_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='config',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='event.taskconfig', verbose_name='업무 종류'),
        ),
        migrations.AlterField(
            model_name='task',
            name='done',
            field=models.BooleanField(default=False, verbose_name='완료 여부'),
        ),
        migrations.AlterField(
            model_name='task',
            name='modify_reason',
            field=models.TextField(blank=True, null=True, verbose_name='수정 이유'),
        ),
        migrations.AlterField(
            model_name='task',
            name='signature',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='사인'),
        ),
        migrations.AlterField(
            model_name='taskconfig',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=18, samples=None, verbose_name='달력에 나타날 색상'),
        ),
        migrations.AlterField(
            model_name='taskconfig',
            name='name',
            field=models.CharField(max_length=30, verbose_name='업무 이름'),
        ),
    ]
