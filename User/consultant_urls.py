from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.ConsultantSignupAPI.as_view(), name='consultant_signup_api'),
    path('login/', views.UserConsultantLoginAPI.as_view(), name='consultant_login_api'),
    path('secretary-request/', views.SecretaryRequestAPI.as_view(), name='crud_secretary_for_consultant'),
    path('secretary-request/<int:requestId>/', views.SecretaryRequestAPI.as_view(), name='delete_secretary_request'),
]