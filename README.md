# factory_monitor
## setup
1. add your host ip in factory_monitor/settings.py
    ALLOW_HOST = ['ip', ]
2. to run: python manage.py runserver 0.0.0.0:(portnum)
3. admin login http://ip:port/admin  
> superuser: admin  
pwd: adminpwd   
email: ryu328@126.com

## users部分
验证码、邮箱未完成， 前端可以处理一下template里面的html
> users/register - templates/users/register.html  
users/login - templates/registration/login.html  
users/password_reset - templates/registration/password_reset_form.html, password_reset_done.html, password_reset_complete.html  
users/password_change - templates/registration/password_change_form.html, templates/registration/password_change_done.html  

