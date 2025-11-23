from django.shortcuts import render

def staff_list(request):
    """Renders the list view for all teachers and staff."""
    return render(request, 'staff/staff_list.html')