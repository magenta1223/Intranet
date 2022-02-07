# Generated by Django 3.2.11 on 2022-02-06 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import picklefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EstimatorType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': '품목',
                'verbose_name_plural': '품목',
            },
        ),
        migrations.CreateModel(
            name='Estimator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(verbose_name='작성일자')),
                ('modify_date', models.DateTimeField(blank=True, null=True, verbose_name='수정일자')),
                ('type', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=200, null=True)),
                ('kwargs', picklefield.fields.PickledObjectField(editable=False)),
                ('additional_kwargs', picklefield.fields.PickledObjectField(editable=False, null=True)),
                ('prices', picklefield.fields.PickledObjectField(editable=False, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'verbose_name': '견적서',
                'verbose_name_plural': '견적서',
            },
        ),
    ]
