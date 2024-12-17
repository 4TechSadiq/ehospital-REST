from django.urls import path
from . import views

urlpatterns = [
    path("create-user", views.UserList.as_view(), name="create-user"),
    path("user/<int:pk>", views.UserDetail.as_view(), name="user-detail"),
    path("list-users", views.ListUser.as_view(), name="list-users"),
    path("create-doctor", views.DoctorList.as_view(), name="create-doctor"),
    path("doctor/<int:pk>", views.DoctorDetail.as_view(), name="doctor-detail"),
    path("create-med-history", views.MedHistoryList.as_view(), name="create-med-history"),
    path("med-history/<int:pk>", views.MedHistoryDetail.as_view(), name="med-history-detail"),
    path("create-heath-status", views.HeathStatusList.as_view(), name="create-heath-status"),
    path("heath-status/<int:pk>", views.HeathStatusDetail.as_view(), name="heath-status-detail"),
    path("create-med-news", views.MedNewsList.as_view(), name="create-med-news"),
    path("med-news/<int:pk>", views.MedNewsDetail.as_view(), name="med-news-detail"),
    path("create-appointment", views.CreateAppointment.as_view(), name="list-med-news"),
    path("list-appointment", views.ListAppointment.as_view(), name="create-appointment"),
    path("remove-appointment/<int:pk>", views.RemoveAppointment.as_view(), name="remove-appointment"),
]