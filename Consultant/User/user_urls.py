from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.UserLoginAPI.as_view(), name='login_api'),
]
