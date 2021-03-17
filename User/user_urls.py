from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.UserSignupAPI.as_view(), name='user_signup_api'),
    path('login/', views.UserLoginAPI.as_view(), name='user_login_api'),
]
