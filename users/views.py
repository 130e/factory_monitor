from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.views import View

from .forms import RegisterForm
from .models import User
from .utils import send_auth_email

import logging


class RegisterView(View):
    def get(self, request):
        empty_form = RegisterForm()
        return render(request, 'registration/registration.html', context={'form': empty_form})

    def post(self, request):
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、确认密码、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)
        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，将用户数据保存到数据库
            user = User()
            user_name = request.POST.get("username", '')
            user_email = request.POST.get("email", '')

            user.username = user_name
            user.email = user_email
            user.password = make_password(form.cleaned_data.get('password1'))
            # 新建为非活跃用户，邮箱验证后变为活跃用户
            user.is_active = False
            user.save()

            # logging
            logger = logging.getLogger('users.register')
            logger.info('New User {0} registered.'.format(user_name))
            logger.info(form.cleaned_data.get('password1'))
            logger.info(user.password)
            
            # 验证邮箱
            send_auth_email(user_name, user_email)
            return redirect('/')
        else:
            return render(request, 'registration/registration.html', context={'form': form})


class ActiveUserView(View):
    def get(self, request, user_name, activate_code):
        # 找到相应用户
        user = User.objects.get(username=user_name)
        if user:
            if activate_code == user.email_code:
                user.is_active = True
                user.save()
                return redirect('/')
        return render(request, "registration/activate_fail.html")
