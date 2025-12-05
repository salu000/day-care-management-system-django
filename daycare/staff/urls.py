from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.staff_list, name='staff_list'),
    path('create/', views.staff_create, name='staff_create'),
    path('<int:pk>/update/', views.staff_update, name='staff_update'),
    path('<int:pk>/delete/', views.staff_delete, name='staff_delete'),
]