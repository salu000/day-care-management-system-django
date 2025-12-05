from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.daily_attendance_view, name='daily_tracker'),
    path('api/update/', views.update_attendance_api, name='update_attendance_api'),
]