from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserSignupAPI.as_view(), name='channel_crud'),
]
