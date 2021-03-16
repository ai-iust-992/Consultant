from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.UserSignupAPI.as_view(), name='login_api'),
]
