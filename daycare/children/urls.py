from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'children'

urlpatterns = [
    path('', views.all_students, name='all_students'),
    path('students/admission/', views.admission_form, name='admission_form'),
    path('students/promotion/', views.student_promotion, name='student_promotion'),
    path('classes/', views.class_list, name='class_list'),
    
    # AJAX / Modal Actions
    path('student/<int:pk>/detail/', views.student_detail_ajax, name='student_detail_ajax'),
    path('student/<int:pk>/delete/', views.student_delete, name='student_delete'),
] 
