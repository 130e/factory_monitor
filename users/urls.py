from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'users' # curcial
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('activate/<user_name>/<activate_code>', views.ActiveUserView.as_view(), name="user_active"),
]