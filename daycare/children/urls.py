from django.urls import path
from . import views

app_name = 'children'

urlpatterns = [
    # Mapped to /children/students/all/
    path('', views.all_students, name='all_students'),
    path('students/all/', views.all_students, name='all_students'),
    # Mapped to /children/students/admission/
    path('students/admission/', views.admission_form, name='admission_form'),
    # Mapped to /children/students/promotion/
    path('students/promotion/', views.student_promotion, name='student_promotion'),
    # Mapped to /children/classes/
    path('classes/', views.class_list, name='class_list'),
]