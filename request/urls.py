from django.urls import path
from . import views

urlpatterns = [
    path('applicant/', views.RequestAPI.as_view(), name='crud_secretary_for_consultant'),
    path('applicant/<int:requestId>/', views.RequestAPI.as_view(), name='delete_secretary_request'),
    path('', views.AnswerToRequestAPI.as_view(),
         name="get all user requests"),
    path('answer/<int:requestId>/', views.AnswerToRequestAPI.as_view(),
         name="answer to  requests"),
]
