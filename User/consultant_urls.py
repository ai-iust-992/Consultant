from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.ConsultantSignupAPI.as_view(), name='consultant_signup_api'),
    path('login/', views.UserConsultantLoginAPI.as_view(), name='consultant_login_api'),
]