from django.urls import path
from . import views

app_name = 'billings'

urlpatterns = [
    path('view/', views.billing_view, name='billing_view'),
    path('generate/', views.generate_invoice, name='generate_invoice'),
    path('api/update-rate/', views.update_child_rate, name='update_child_rate'),
    path('invoice/pdf/<int:invoice_id>/', views.invoice_pdf_view, name='invoice_pdf'),
    # API Routes for Modals
    path('api/details/<int:invoice_id>/', views.get_invoice_details, name='invoice_details'),
    path('api/update/', views.update_invoice_payment, name='update_payment'),
]