# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-02-26 16:49
from __future__ import unicode_literals

import ask_students.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=4096)),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
                ('posted', models.DateTimeField()),
                ('edited', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.CharField(max_length=512)),
                ('approved', models.BooleanField(default=False)),
                ('slug', models.SlugField(unique=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='PlaceOfStudy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('test', models.CharField(max_length=4096)),
                ('anonymous', models.BooleanField()),
                ('posted', models.DateTimeField()),
                ('edited', models.DateTimeField()),
                ('views', models.IntegerField(default=0)),
                ('support_file', models.ImageField(null=True, upload_to='support_files')),
                ('answered', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ask_students.Answer')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ask_students.Category')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=4096)),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
                ('image', models.ImageField(upload_to='profile_images')),
                ('permission', models.ForeignKey(default=ask_students.models.default_student, on_delete=django.db.models.deletion.SET_DEFAULT, to='ask_students.Permission')),
                ('place_of_study', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ask_students.PlaceOfStudy')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ask_students.UserProfile'),
        ),
        migrations.AddField(
            model_name='answer',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ask_students.Category'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ask_students.UserProfile'),
        ),
    ]
