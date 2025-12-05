from django.urls import path
from . import views

app_name = 'guardians'

urlpatterns = [
    path('', views.guardian_list, name='guardian_list'),
    
    # AJAX Actions
    path('guardian/<int:pk>/detail/', views.guardian_detail_ajax, name='guardian_detail_ajax'),
    path('guardian/<int:pk>/delete/', views.guardian_delete, name='guardian_delete'),
]