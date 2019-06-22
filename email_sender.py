import smtplib
from email.mime.text import MIMEText
import datetime
import re

def sendEmail(data):

    # 第三方 SMTP 服务
    mail_host = "smtp.163.com"  # SMTP服务器
    mail_user = "wshao0904@163.com"  # 用户名
    mail_pass = "welcome2dow"  # 授权密码，非登录密码

    sender = 'wshao0904@163.com'  # 发件人邮箱
    receivers = ['wshao0904@163.com']  # 接收邮件

    content_all = data.to_html(escape=False,index=False)
    content_link = data.iloc[:,[5,8]].to_html()
    content1 = re.findall('<td>(?!http)(.*?)</td>',content_link)
    content2 = re.findall('<td>(http.*?)</td>',content_link)
    for i in range(len(data)):
        rep = """<td><a href="{}">{}</td>""".format(content2[i],content1[i])
        regex = """<td>{}</td>""".format(content2[i])
        content_all = re.sub(regex,rep,content_all)

    with open(r'C:\Users\Neo\Desktop\test1.txt', 'w') as f:
        f.write(content_all)

    title = str(datetime.date.today()) + ' 新增职位 ' + str(data.shape[0]) + ' 个' # 邮件主题
    message = MIMEText(content_all, 'html', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("成功发送邮件")
    except smtplib.SMTPException as e:
        print(e)

