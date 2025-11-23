from django.urls import path
from . import views

app_name = 'guardians'

urlpatterns = [
    # Mapped to /guardians/list/
    path('', views.guardian_list, name='guardian_list'),
]