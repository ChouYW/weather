# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 09:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0007_auto_20170928_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='cityId',
            field=models.CharField(default='', max_length=32, verbose_name='城市id'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='email',
            field=models.CharField(default='', max_length=32, verbose_name='接收消息邮箱'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='openId',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AddField(
            model_name='weatherinfo',
            name='content',
            field=models.CharField(default='', max_length=4000, verbose_name='发送内容'),
        ),
        migrations.AddField(
            model_name='weatherinfo',
            name='title',
            field=models.CharField(default='', max_length=400, verbose_name='发送标题'),
        ),
        migrations.AlterField(
            model_name='weatherinfo',
            name='temdate',
            field=models.DateField(default=datetime.datetime(2017, 9, 28, 9, 34, 29, 761488, tzinfo=utc), verbose_name='日期'),
        ),
    ]