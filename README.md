# factory_monitor
UESTC, 2018 
**Classroom project**

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

## machine部分
### API
**污水进出控制器(Controler):**
> GET api/machine/controler/time/latest/ \
得到最新的json格式数据{'timestamp':"2018-06-02T16:44:38.481047+08:00",'water_in':float,'water_out':float,'COD':float,'BOD':float} \
数据名称：timestamp 时间戳    water_in 进水流量    water_out 出水流量  COD  出水COD    BOD 出水BOD
>
> GET api/machine/controler/time/   params:year,month,day
> 得到year-month-day当天的所有数据，格式和名称同上

**污水处理器(Processor):**
> GET api/machine/processor/time/latest/ \
> 得到最新的json格式数据{'timestamp':"2018-06-02T16:44:38.481047+08:00",'level':float,'temperature':float,'PH':float,'density':float} \
> 数据名称：timestamp 时间戳    level 提升泵液位    temperature 曝气池温度    PH 曝气池PH    density 污泥浓度

> GET api/machine/processor/time/    params:year,month,day
> 得到year-month-day当天的所有数据，格式和名称同上


