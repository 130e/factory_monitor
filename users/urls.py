from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'users' # curcial
urlpatterns = [
    # url(r'^register/', views.RegisterView.as_view(), name='register'),
    # url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('active/<user_name>/<int:active_code>', views.ActiveUserView.as_view(), name="user_active"),
]