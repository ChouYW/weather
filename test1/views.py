#coding=utf-8
from django.shortcuts import render
import urllib.request
import urllib.parse
from test1 import models
from bs4 import BeautifulSoup
from django.utils import timezone
import smtplib
from email.mime.text import MIMEText
import json


def index(request):
    return render(request, "index.html")

# 更新城市代码
def updateCity(request):
    city_list = models.CityInfo.objects.all()
    for city in city_list:
        # 调用中国天气API获取城市天气页面代码
        url = "http://toy1.weather.com.cn/search?cityname="+ urllib.parse.quote(city.name)
        with urllib.request.urlopen(url) as f:
            info = f.read().decode('utf-8')[1:-1]
            result = json.loads(info)
            cityId = result[0]["ref"].split("~")[0]
            city.cityId = cityId
            city.save()
    return render(request, "index.html")

# 更新天气信息
def updateWeather(request):
    city_list = models.CityInfo.objects.all()
    for city in city_list:
        url = "http://www.weather.com.cn/weather/"+ city.cityId +".shtml"
        html = getHtml(url,0)
        soup = BeautifulSoup(html, 'html.parser')
        # 获取天气信息
        ul = soup.find(class_="t clearfix")
        if ul:
            weas = ul.find_all(class_="wea")
            todayWea = weas[0].text
            tomWea = weas[1].text
            afterTomWea = weas[2].text
            minTem = ul.find_all(class_="tem")[0].find('i').text[0:-1]
            maxTem = ul.find_all(class_="tem")[0].span.text
            wind = ul.find_all(class_="win")[0].i.text
            # 拼接发送消息标题和内容
            title = todayWea
            content = u'早上好，今天天气是{wea}。温度{tem}，风力：{win}。{rain}'
            if u'雨' in title:
                title += u'，记得带伞哦'

            content = content.replace('{wea}', title)

            if minTem:
                content = content.replace('{tem}', minTem +'℃~'+ maxTem +'℃')
            else:
                content = content.replace('{tem}', maxTem +'℃')

            content = content.replace('{win}',wind)

            # 替换{rain}（描述明后天是否下雨）
            if u'雨' in tomWea:
                content = content.replace('{rain}', u'明天将会有雨，到时记得带伞哦。')
            elif u'雨' in afterTomWea:
                content = content.replace('{rain}', u'后天将会有雨，到时记得带伞哦。')
            else:
                content = content.replace('{rain}', '')
            #  保存到数据库
            models.WeatherInfo.objects.create(cityId=city.cityId,minTem=minTem,maxTem=maxTem,wind=wind,
                                              todayWea=todayWea,tomWea=tomWea,afterTomWea=afterTomWea,
                                              title=title,content=content,temdate=timezone.now())

    return render(request, "index.html")

def getHtml(url, times):
    if ++times > 10:
        return ""
    try:
        return urllib.request.urlopen(url,timeout=4).read()
    except:
        return getHtml(url, times)

# 发送消息给订阅的用户
def sendMessage(request):
    city_list = models.CityInfo.objects.all()
    for city in city_list:
        user_list = models.UserInfo.objects.filter(cityId=city.cityId)
        weather = models.WeatherInfo.objects.get(cityId=city.cityId,temdate=timezone.now().date())
        for user in user_list:
            sendEmail(weather.content, user.email, weather.title)
    return render(request, "index.html")

def sendEmail(content, touser, title):
    if not content or not touser or not title:
        return
    # 163邮箱服务器地址
    mail_host = 'smtp.163.com'
    mail_user = 'z406245159'
    mail_pass = 'Z123456789z'
    sender = 'z406245159@163.com'
    receivers = [touser]

    # 设置内容
    message = MIMEText(content, 'plain', 'utf-8')
    fromuser =mail_user + '<'+ sender + '>'
    message['From'] = fromuser
    message['To'] = receivers[0]
    message['Subject'] = title

    # 发送邮件
    server = smtplib.SMTP(mail_host, 25)
    server.set_debuglevel(1)
    server.login(mail_user, mail_pass)
    server.sendmail(sender, receivers, message.as_string())