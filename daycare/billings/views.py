from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum, Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.template.loader import get_template # Changed for xhtml2pdf
import json
from datetime import datetime, timedelta

# NEW LIBRARY (Easier for Windows)
from xhtml2pdf import pisa 

from .models import Invoice
from children.models import Child
from attendance.models import Attendance

@login_required
def billing_view(request):
    """Main Dashboard"""
    invoices = Invoice.objects.all().order_by('-created_at')
    
    # Calculate Dashboard Metrics
    total_unpaid = invoices.filter(~Q(status='PAID')).aggregate(
        total=Sum('total_amount') - Sum('amount_paid')
    )['total'] or 0
    
    due_soon = invoices.filter(
        status='UNPAID', 
        due_date__lte=timezone.now().date() + timedelta(days=7)
    ).count()

    context = {
        'invoices': invoices,
        'total_unpaid': total_unpaid,
        'due_soon': due_soon,
        'children': Child.objects.filter(status='Active') # For the create dropdown
    }
    return render(request, 'billings/billing_view.html', context)

@login_required
@require_POST
def generate_invoice(request):
    try:
        child_id = request.POST.get('child_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        due_date = request.POST.get('due_date')
        
        child = get_object_or_404(Child, id=child_id)
        
        # DEBUGGING
        print(f"Generating for: {child.full_name} ({start_date} to {end_date})")
        
        # 1. Calculate Attendance Count
        attendance_records = Attendance.objects.filter(
            child=child,
            date__range=[start_date, end_date],
            status='PRESENT'
        )
        
        present_days = attendance_records.count()
        print(f"Found {present_days} present days")

        # 2. Calculate Cost
        rate = child.default_daily_rate
        if rate <= 0:
            print("WARNING: Child has 0 rate")
            
        base_amount = present_days * rate
        
        # 3. Create Invoice
        Invoice.objects.create(
            child=child,
            period_start=start_date,
            period_end=end_date,
            due_date=due_date,
            total_days_present=present_days,
            daily_rate_applied=rate,
            base_amount=base_amount,
            total_amount=base_amount 
        )
        
        return redirect('billings:billing_view')
    except Exception as e:
        print(f"Error generating invoice: {e}")
        return redirect('billings:billing_view')

@login_required
def get_invoice_details(request, invoice_id):
    """API for the Popup Modal"""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    data = {
        'id': invoice.id,
        'child_name': invoice.child.full_name,
        'guardian_email': invoice.child.guardian.email, 
        'period': f"{invoice.period_start} to {invoice.period_end}",
        'days': invoice.total_days_present,
        'rate': float(invoice.daily_rate_applied),
        'base': float(invoice.base_amount),
        'adjustment': float(invoice.adjustment_amount),
        'reason': invoice.adjustment_reason,
        'total': float(invoice.total_amount),
        'paid': float(invoice.amount_paid),
        'balance': float(invoice.get_balance_due()),
        'status': invoice.status,
    }
    return JsonResponse(data)

def safe_float(value):
    """Helper to convert string to float safely, handling empty strings."""
    if not value:
        return 0.0
    try:
        return float(value)
    except ValueError:
        return 0.0

@login_required
@require_POST
def update_invoice_payment(request):
    """API to add payment or adjust Invoice"""
    try:
        data = json.loads(request.body)
        invoice_id = data.get('invoice_id')
        
        if not invoice_id:
             return JsonResponse({'success': False, 'error': 'No Invoice ID provided'}, status=400)

        invoice = get_object_or_404(Invoice, id=invoice_id)
        
        # 1. Handle Payment
        payment_input = data.get('payment_amount')
        payment_amount = safe_float(payment_input)
        
        if payment_amount != 0:
            invoice.amount_paid = float(invoice.amount_paid) + payment_amount

        # 2. Handle Adjustment
        adjustment_input = data.get('adjustment_amount')
        new_adjustment = safe_float(adjustment_input)
        adjustment_reason = data.get('adjustment_reason', '')
        
        # Only update adjustment if user actually typed something
        if adjustment_input and adjustment_input != "": 
            invoice.adjustment_amount = new_adjustment
            invoice.adjustment_reason = adjustment_reason

        invoice.save() 
        
        return JsonResponse({'success': True})

    except Exception as e:
        print(f"Error in update_invoice_payment: {e}") 
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_POST
def update_child_rate(request):
    """API to update student daily rate from the Dashboard UI"""
    try:
        data = json.loads(request.body)
        child_id = data.get('child_id')
        new_rate = data.get('rate')
        
        child = get_object_or_404(Child, id=child_id)
        child.default_daily_rate = float(new_rate)
        child.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
def invoice_pdf_view(request, invoice_id):
    """Generates a PDF for a specific invoice using xhtml2pdf"""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    template_path = 'billings/invoice_pdf.html'
    context = {
        'invoice': invoice,
        'user': request.user,
    }
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # Change 'inline' to 'attachment' if you want to force download instead of viewing
    response['Content-Disposition'] = f'inline; filename="invoice_{invoice.id}.pdf"'
    
    # Find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # Create the PDF
    pisa_status = pisa.CreatePDF(
       html, dest=response
    )

    # If error
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
       
    return response