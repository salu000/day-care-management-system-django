from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    # Existing Tracker URLs
    path('', views.activity_tracker, name='tracker'),
    path('api/add/', views.add_activity_api, name='add_api'),
    
    # New Schedule URL
    path('schedule/', views.schedule_list, name='schedule_list'),
]