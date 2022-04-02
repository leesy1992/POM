import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os

from Autotest_platform.settings import EMAIL_SEND_USERNAME, EMAIL_SEND_PASSWORD
# EMAIL_SEND_USERNAME = 'charles.li@ihr360.com'  # 定时任务报告发送邮箱，支持163,qq,sina,企业qq邮箱等，注意需要开通smtp服务
# EMAIL_SEND_PASSWORD = 'Sdjk9898'     # 邮箱密码


def send_email_reports(splitResult_id,receiver='charles.li@ihr360.com', name="",subject=" UI自动化测试报告", bodyText="UI测试报告地址： ",status="【成功】"):
    if '@sina.com' in EMAIL_SEND_USERNAME:
        smtp_server = 'smtp.sina.com'
    elif '@163.com' in EMAIL_SEND_USERNAME:
        smtp_server = 'smtp.163.com'
    elif '@ihr360.com' in EMAIL_SEND_USERNAME or '@cnbexpress.com' in EMAIL_SEND_USERNAME:
        smtp_server = 'smtp.mxhichina.com'
    else:
        smtp_server = 'smtp.exmail.qq.com'

    subject = status+"_"+name+"_"+subject
    # body="<p>{}<a href='http://127.0.0.1:8000/admin/results/{}'>http://127.0.0.1:8000/admin/results/{}</a>    请查收，谢谢！</p>".format(bodyText,splitResult_id,splitResult_id)#本地地址
    body="<p>{}<a href='http://192.168.1.201:8000/admin/results/{}'>http://127.0.0.1:8000/admin/results/{} </a>    请查收，谢谢！</p>".format(bodyText,splitResult_id,splitResult_id)#线上地址

    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['from'] = EMAIL_SEND_USERNAME
    msg['to'] = receiver

    smtp = smtplib.SMTP()
    smtp.connect(smtp_server)
    smtp.starttls()
    smtp.login(EMAIL_SEND_USERNAME, EMAIL_SEND_PASSWORD)
    smtp.sendmail(EMAIL_SEND_USERNAME, receiver.split(','), msg.as_string())
    smtp.quit()


if __name__ == '__main__':

   send_email_reports(2606,name="测试")
    # pass
