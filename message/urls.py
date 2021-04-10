from django.urls import path
from . import views

urlpatterns = [
    path('', views.MessageAPI.as_view(), name='message_crud'),
]