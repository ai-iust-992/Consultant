from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChannelAPI.as_view(), name='channel_crud'),
]
