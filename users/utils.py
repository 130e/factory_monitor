from random import Random # 用于生成随机码 
from django.core.mail import EmailMessage, send_mail # 发送邮件模块
from .models import User
from datetime import datetime 

# 生成随机字符串
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)] #slow
    return str


def send_auth_email(name, email):
    # 将生成的验证码保存在数据库
    code = random_str(16)
    user = User.objects.get(username=name)
    user.email_code = code
    user.save()
    # 初始化为空
    email_title = ""
    email_body = ""
    # 如果为注册类型
    email_title = "Factory项目-注册激活链接"
    email_body = "Hello {}, \n".format(name)
    email_body += "请点击下面的链接激活你的账号: http://106.15.230.111/users/activate/{0}/{1}".format(name, code)
    email_body += "\n TheGreatNet Group {}".format(datetime.now())
    # 发送邮件
    emailmsg = EmailMessage(subject=email_title, body=email_body, to=[email])
    from_mail = "cjt1256182832@aliyun.com"
    send_status = send_mail(email_title, email_body, from_mail, [email])
    if send_status:
        pass