from random import Random # 用于生成随机码 
from django.core.mail import send_mail # 发送邮件模块
from users.models import EmailRecord # 邮箱验证model
from datetime import datetime

EMAIL_FROM = "ryu328@126.com" 

# 生成随机字符串
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)] #slow
    return str


def send_auth_email(name, email, send_type="register"):
    email_record = EmailRecord()
    # 将给用户发的信息保存在数据库中
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    # 初始化为空
    email_title = ""
    email_body = ""
    # 如果为注册类型
    if send_type == "register":
        email_title = "Factory项目-注册激活链接"
        email_body = "Hello {}, \n".format(name)
        email_body += "请点击下面的链接激活你的账号: http://140.82.18.139:8000/users/activate/{0}/{1}".format(name, code)
        email_body += "\n TheGreatNet Group {}".format(datetime.now())
        # 发送邮件
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            # success
            pass