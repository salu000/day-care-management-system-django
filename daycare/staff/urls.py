from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    # Mapped to /staff/teachers/
   path('', views.staff_list, name='staff_list'),
]