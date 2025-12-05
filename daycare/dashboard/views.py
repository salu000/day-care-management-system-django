from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import timedelta

# Import your models
from children.models import Child
from attendance.models import Attendance
from billings.models import Invoice

@login_required
def dashboard_index(request):
    today = timezone.now().date()
    
    # --- 1. STUDENT METRICS ---
    total_students = Child.objects.filter(status='Active').count()
    # Students added in last 30 days
    new_admissions = Child.objects.filter(
        start_date__gte=today - timedelta(days=30)
    ).count()

    # --- 2. ATTENDANCE METRICS (TODAY) ---
    today_attendance = Attendance.objects.filter(date=today)
    present_today = today_attendance.filter(status='PRESENT').count()
    absent_today = today_attendance.filter(status='ABSENT').count()
    on_leave = today_attendance.filter(status='LEAVE').count()
    
    # Calculate Attendance %
    attendance_rate = 0
    if total_students > 0:
        attendance_rate = round((present_today / total_students) * 100)

    # --- 3. FINANCIAL METRICS ---
    # Calculate Total Outstanding (Total Amount - Amount Paid) for unpaid invoices
    financials = Invoice.objects.filter(~Q(status='PAID')).aggregate(
        pending=Sum('total_amount') - Sum('amount_paid')
    )
    total_pending = financials['pending'] or 0

    # --- 4. CHART DATA (Last 7 Days) ---
    # We need two lists: Labels (Dates) and Data (Present Counts)
    chart_labels = []
    chart_data = []
    
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        # Label: "Mon", "Tue"
        chart_labels.append(date.strftime('%a')) 
        # Data: Count of 'PRESENT'
        count = Attendance.objects.filter(date=date, status='PRESENT').count()
        chart_data.append(count)

    context = {
        'total_students': total_students,
        'new_admissions': new_admissions,
        'present_today': present_today,
        'absent_today': absent_today,
        'on_leave': on_leave,
        'attendance_rate': attendance_rate,
        'total_pending': total_pending,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'dashboard/index.html', context)