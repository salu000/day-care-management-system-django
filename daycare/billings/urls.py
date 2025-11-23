from django.urls import path
from . import views

app_name = 'billings'

urlpatterns = [
    # Mapped to /billing/view/
    path('view/', views.billing_view, name='billing_view'),
]