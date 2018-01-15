from django.db import models
from django.utils import timezone

class UserInfo(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    openId = models.CharField(max_length=32, default="")
    # 城市id
    cityId = models.CharField('城市id', max_length=32, default="")
    # 接收消息邮箱
    email = models.CharField('接收消息邮箱', max_length=32, default="")

class CityInfo(models.Model):
    name = models.CharField(max_length=32)
    cityId = models.CharField(max_length=32)

class WeatherInfo(models.Model):
    # 城市id
    cityId = models.CharField('城市id', max_length=32)
    # 最低温度
    minTem = models.CharField('最低温度', max_length=32)
    # 最高温度
    maxTem = models.CharField('最高温度', max_length=32)
    # 风向
    wind = models.CharField('风向',default="", max_length=32)
    # 今天天气
    todayWea = models.CharField('今天天气', max_length=32)
    # 明天天气
    tomWea = models.CharField('明天天气', max_length=32)
    # 后天天气
    afterTomWea = models.CharField('后天天气', max_length=32)
    # 发送标题
    title = models.CharField('发送标题',default="", max_length=400)
    # 发送内容
    content = models.CharField('发送内容',default="", max_length=4000)
    # 日期
    temdate = models.DateField("日期",default=timezone.now())