#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:zhangcong
# Email:zc_92@sina.com

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def mail(to_list, subject, text):
    """
    发邮件
    :param to_list: # 一个列表  需要发送邮件的邮箱列表
    :param subject: # 邮件标题
    :param text: # 邮件内容
    :return:
    """

    # 发件人
    _user = "xxx@xxx.com"
    # 密码
    _pwd = "xxx"
    # 收件人 _to = ["xxx@xxx.com", "xxx@xxx.com"] 多个收件人
    _to = to_list
    # 邮件标题
    Subject = subject
    # 邮件文本内容
    Text = text

    # 如名字所示Multipart就是分多个部分
    msg = MIMEMultipart()
    msg["Subject"] = Subject
    msg["From"] = _user
    msg["To"] = ",".join(_to)

    # ---这是文字部分---
    part = MIMEText(Text, 'plain', 'utf-8')
    msg.attach(part)

    # ---这是附件部分 如果不需要附件可以注释掉---
    # 文件类型附件
    # part = MIMEApplication(open('./ym.txt', 'rb').read())
    # part.add_header('Content-Disposition', 'attachment', filename="/data/zhangcong/script/python/project/ym.txt")
    # msg.attach(part)

    # #jpg类型附件
    # part = MIMEApplication(open('foo.jpg','rb').read())
    # part.add_header('Content-Disposition', 'attachment', filename="foo.jpg")
    # msg.attach(part)
    #
    # #pdf类型附件
    # part = MIMEApplication(open('foo.pdf','rb').read())
    # part.add_header('Content-Disposition', 'attachment', filename="foo.pdf")
    # msg.attach(part)
    #
    # #mp3类型附件
    # part = MIMEApplication(open('foo.mp3','rb').read())
    # part.add_header('Content-Disposition', 'attachment', filename="foo.mp3")
    # msg.attach(part)

    # 连接smtp邮件服务器,端口默认是25
    s = smtplib.SMTP("smtp_server", timeout=30)  # smtp_server是你发件人得smtp服务器地址
    # 登陆服务器
    s.login(_user, _pwd)
    # 发送邮件
    s.sendmail(_user, _to, msg.as_string())
    s.close()


if __name__ == '__main__':
    to_list = ["xxx@qq.com"]  # 收件人列表,
    subject = "测试"
    text = "测试邮件"
    mail(to_list, subject, text)