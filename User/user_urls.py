from django.urls import path
from . import views
from  channel.views import UserChannelsAPI, UserRoleInChannelAPI

urlpatterns = [
    path('signup/', views.UserSignupAPI.as_view(), name='user_signup_api'),
    path('login/', views.UserConsultantLoginAPI.as_view(), name='user_login_api'),
    path('channels/', UserChannelsAPI.as_view(), name='user_channels'),
    path('channel-role/<int:channelId>/', UserRoleInChannelAPI.as_view(), name='user_channels'),
]
