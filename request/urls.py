from django.urls import path
from . import views

urlpatterns = [
    path('secretary-request/', views.SecretaryRequestAPI.as_view(), name='crud_secretary_for_consultant'),
    path('secretary-request/<int:requestId>/', views.SecretaryRequestAPI.as_view(), name='delete_secretary_request'),
    path('join-channel-request/<int:channelId>/', views.JoinChannelRequestAPI.as_view(),
         name="create and get join channel requests"),
    path('join-channel-request/<int:channelId>/<int:requestId>/', views.JoinChannelRequestAPI.as_view(),
         name="delete join channel requests"),
    path('', views.AnswerToRequestAPI.as_view(),
         name="get all user requests"),
    path('answer/<int:requestId>/', views.AnswerToRequestAPI.as_view(),
         name="answer to  requests"),
]
