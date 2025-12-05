from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.db.models import Q
from .models import StaffMember
from .forms import StaffForm

def staff_list(request):
    """Lists all staff with search functionality."""
    staff_members = StaffMember.objects.all().order_by('-date_joined')

    # Search Logic
    query = request.GET.get('q')
    if query:
        staff_members = staff_members.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(email__icontains=query) |
            Q(role__icontains=query)
        )

    context = {
        'staff_members': staff_members,
        'form': StaffForm() # Empty form for the "Add New" modal
    }
    return render(request, 'staff/staff_list.html', context)

def staff_create(request):
    """Handles adding a new staff member via Modal POST."""
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "New staff member added successfully!")
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def staff_update(request, pk):
    """Returns Edit Form (GET) and Handles Update (POST) via AJAX."""
    staff = get_object_or_404(StaffMember, pk=pk)

    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff details updated!")
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    
    # If GET, return the form HTML to populate the modal
    form = StaffForm(instance=staff)
    html = render_to_string('staff/partials/staff_form_modal.html', {
        'form': form,
        'staff': staff, # Pass instance to check ID in template
    }, request=request)
    return JsonResponse({'html': html})

def staff_delete(request, pk):
    """Deletes a staff member."""
    if request.method == 'POST':
        staff = get_object_or_404(StaffMember, pk=pk)
        staff.delete()
        messages.success(request, "Staff member removed.")
        return redirect('staff:staff_list')