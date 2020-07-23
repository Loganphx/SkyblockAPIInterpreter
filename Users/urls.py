from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('get_user/<username>', views.get_user, name='get user info'),
    path('resetpassword', views.email_reset, name='Reset Password'),
]
