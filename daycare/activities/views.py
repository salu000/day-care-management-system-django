from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
import json
from datetime import datetime

from children.models import Child
from .models import DailyActivity, ScheduleItem

# --- EXISTING VIEW: Activity Tracker ---
@login_required
def activity_tracker(request):
    """Main view to list students and their daily timeline"""
    today = timezone.now().date()
    
    # Get all active children
    children = Child.objects.filter(status='Active').order_by('full_name')
    
    # Attach today's activities to each child object
    child_data = []
    for child in children:
        activities = DailyActivity.objects.filter(child=child, date=today).order_by('time')
        child_data.append({
            'info': child,
            'activities': activities
        })

    context = {
        'child_data': child_data,
        'today': today
    }
    return render(request, 'activities/activity_tracker.html', context)

# --- EXISTING API: Save Log ---
@login_required
@require_POST
def add_activity_api(request):
    """AJAX endpoint to save an activity"""
    try:
        data = json.loads(request.body)
        child_id = data.get('child_id')
        activity_type = data.get('activity_type')
        title = data.get('title')
        description = data.get('description')
        time_str = data.get('time') # HH:MM format

        child = get_object_or_404(Child, id=child_id)
        
        DailyActivity.objects.create(
            child=child,
            activity_type=activity_type,
            title=title,
            description=description,
            date=timezone.now().date(),
            time=time_str
        )
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

# --- NEW VIEW: Class Schedule ---
@login_required
def schedule_list(request):
    """Renders the Daily Activity Schedule Wireframe"""
    
    # Fetch all items
    schedules = ScheduleItem.objects.all()
    
    # Group them for the tabs
    context = {
        'infant_schedule': schedules.filter(group='INFANT'),
        'toddler_schedule': schedules.filter(group='TODDLER'),
        'preschool_schedule': schedules.filter(group='PRESCHOOL'),
    }
    return render(request, 'activities/schedule_list.html', context)