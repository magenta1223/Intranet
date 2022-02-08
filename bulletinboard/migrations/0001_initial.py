# Generated by Django 3.2.11 on 2022-02-06 08:29

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='이름')),
            ],
            options={
                'verbose_name': '카테고리',
                'verbose_name_plural': '카테고리',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(verbose_name='작성일자')),
                ('modify_date', models.DateTimeField(blank=True, null=True, verbose_name='수정일자')),
                ('title', models.CharField(max_length=200, verbose_name='제목')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='내용')),
            ],
            options={
                'verbose_name': '게시글',
                'verbose_name_plural': '게시글',
            },
        ),
    ]