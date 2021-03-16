from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.ConsultantSignupAPI.as_view(), name='login_api'),
]