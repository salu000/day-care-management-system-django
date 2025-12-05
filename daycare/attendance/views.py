from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
import json
from datetime import datetime

# Import models
from .models import Attendance
from children.models import Child

@login_required
def daily_attendance_view(request):
    # 1. Get the date from query params or default to today
    date_str = request.GET.get('date')
    if date_str:
        current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        current_date = timezone.now().date()

    # 2. AUTOMATION: Ensure records exist for this date
    # We wrap this in a transaction to ensure data integrity
    with transaction.atomic():
        # Get all active children
        # Assuming your Child model has 'is_active' or similar. If not, remove the filter.
        active_children = Child.objects.all() 
        print(active_children)
        # Check which children already have attendance for this date
        existing_records = Attendance.objects.filter(date=current_date).values_list('child_id', flat=True)
        print(existing_records)
        # Create 'Absent' records for missing children
        new_attendance_objects = []
        for child in active_children:
            if child.id not in existing_records:
                new_attendance_objects.append(
                    Attendance(
                        child=child, 
                        date=current_date, 
                        status='ABSENT'
                    )
                )
        
        # Bulk create is faster than looping save()
        if new_attendance_objects:
            Attendance.objects.bulk_create(new_attendance_objects)

    # 3. Fetch the full list for the template
    attendance_list = Attendance.objects.filter(date=current_date).select_related('child')

    context = {
        'attendance_list': attendance_list,
        'current_date': current_date.strftime('%Y-%m-%d'),
        'today': timezone.now().date().strftime('%Y-%m-%d')
    }
    return render(request, 'attendance/daily_tracker.html', context)

@login_required
@require_POST
def update_attendance_api(request):
    """
    AJAX Endpoint to update attendance status or time instantly
    """
    try:
        data = json.loads(request.body)
        attendance_id = data.get('id')
        field = data.get('field') # 'status', 'check_in_time', or 'check_out_time'
        value = data.get('value')

        record = get_object_or_404(Attendance, id=attendance_id)

        if field == 'status':
            record.status = value
            # Auto-set check-in time if marked Present and no time exists
            if value == 'PRESENT' and not record.check_in_time:
                record.check_in_time = timezone.now().time()
            # Clear times if marked Absent
            elif value == 'ABSENT':
                record.check_in_time = None
                record.check_out_time = None
        
        elif field == 'check_in_time':
            record.check_in_time = value if value else None
            
        elif field == 'check_out_time':
            record.check_out_time = value if value else None

        record.save()
        
        return JsonResponse({'success': True, 'message': 'Saved'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)