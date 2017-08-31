# -*- coding: utf-8 -*-
import smtplib  # 加载smtplib模块
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from spider_qs import QiuBai
import datetime
"""
    发邮件的方法, 支持发多个人, 支持html和纯文本格式
    author: Roger
"""

mail_text = QiuBai().get_beautiful_html()

def get_subject():
    now_hour = int(datetime.datetime.now().strftime('%H'))
    if 0 <= now_hour <3:
        return '深夜, 晚安'
    elif 3 <= now_hour < 7:
        return '凌晨, 早安'
    elif 7 <= now_hour < 11:
        return '上午好, 今天又是元气满满的一天呢!'
    elif 11 <= now_hour < 13:
        return '中午好, 休息一下吧!'
    elif 13 <= now_hour < 18:
        return '下午, 准备下班!'
    elif 18 <= now_hour < 23:
        return '晚上好, 累了一天, 辛苦了!'
    else:
        return '深夜, 晚安'


SMTP_IP = 'smtp.163.com'  # 邮箱服务器
SMTP_PORT = 25  # 端口

SENDER_INFO = {
    'sender': '******@163.com',  # 发件人邮箱账号
    'password': '******',
    'sender_nickname': '',  # 如果不传则显示发件人的邮箱
}

# 收件人邮箱账号
RECEIVERS = [
    ('XX', '***@163.com'),
]

MAIL_INFO = {
    'subject': '今天天气不错',
    'mail_text': '今天天气不错',
    'mail_type': 'plain',
}

MAIL_INFO = {
    'subject': get_subject(),
    'mail_text': mail_text,
    'mail_type': 'html',
}

FILES = [
]

def get_smtp_server():
    return SMTP_IP, SMTP_PORT


def mail(sender_info, receivers, mail_info, att_paths=None):
    smtp_ip, smtp_port = get_smtp_server()  # 获取连接信息

    subject = mail_info['subject']
    mail_text = mail_info['mail_text']
    mail_type = mail_info['mail_type']  # plain 纯文本; html, html,

    if att_paths:
        msg = MIMEMultipart()
        msg.attach(MIMEText(mail_text, mail_type, 'utf-8'))
    else:
        msg = MIMEText(mail_text, mail_type, 'utf-8')

    sender_nickname = sender_info['sender_nickname']
    sender = sender_info['sender']
    password = sender_info['password']

    if att_paths:
        for att_path in att_paths:
            att = MIMEText(open(att_path, 'rb').read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="%s"' % att_path.split('/')[-1]
            msg.attach(att)

    # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['From'] = formataddr([sender_nickname, sender])
    receiver_mails = []

    for nick_name, receive_mail in receivers:
        # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        receiver_mails.append(receive_mail)

    msg['To'] = ','.join(receiver_mails)
    msg['Subject'] = subject  # 邮件的主题，也可以说是标题

    res = True
    try:
        server = smtplib.SMTP(smtp_ip, smtp_port)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(sender, password)  # 括号中对应的是发件人邮箱账号、邮箱密码
        # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.sendmail(sender, receiver_mails, msg.as_string())
        server.quit()  # 关闭连接
    except smtplib.SMTPException, e:
        print e
        res = False
    return res


def send_mail():
    res = mail(SENDER_INFO, RECEIVERS, MAIL_INFO, FILES)
    if res:
        print 'OK'
    else:
        print 'FAIL'

send_mail()
