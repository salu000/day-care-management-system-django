import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.template.loader import render_to_string
from .models import Child, Guardian
from .forms import ChildForm, GuardianForm

def admission_form(request):
    """Handles creating a new student and their guardian."""
    if request.method == 'POST':
        c_form = ChildForm(request.POST, request.FILES)
        g_form = GuardianForm(request.POST, request.FILES)
        
        if c_form.is_valid() and g_form.is_valid():
            guardian = g_form.save()
            child = c_form.save(commit=False)
            child.guardian = guardian
            child.save()
            messages.success(request, f'Successfully enrolled {child.full_name}!')
            return redirect('children:all_students')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        c_form = ChildForm()
        g_form = GuardianForm()

    return render(request, 'children/admission_form.html', {
        'c_form': c_form, 
        'g_form': g_form
    })

def all_students(request):
    """Lists students with Search, Filter, and CSV Export."""
    students = Child.objects.all().select_related('guardian').order_by('-id')

    # 1. Search (Name or ID)
    search_query = request.GET.get('q')
    if search_query:
        # Check if searching by ID (e.g. #1005) or Name
        if search_query.startswith('#') and search_query[1:].isdigit():
            pk_search = int(search_query[1:]) - 1000
            students = students.filter(id=pk_search)
        else:
            students = students.filter(
                Q(full_name__icontains=search_query) | 
                Q(guardian__name__icontains=search_query)
            )

    # 2. Filter by Class
    class_filter = request.GET.get('class_idx')
    if class_filter and class_filter != 'Filter by Class':
        students = students.filter(enrollment_class=class_filter)

    # 3. Export CSV
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="students_list.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'Class', 'Guardian', 'Phone', 'Status'])
        for s in students:
            writer.writerow([s.get_student_id(), s.full_name, s.enrollment_class, s.guardian.name, s.guardian.phone, s.status])
        return response

    context = {
        'students': students,
        'total_count': students.count(),
        'active_filter': class_filter
    }
    return render(request, 'children/all_students.html', context)

# --- AJAX Views for Modal ---

def student_detail_ajax(request, pk):
    """Returns the Edit form html for the modal"""
    student = get_object_or_404(Child, pk=pk)
    
    if request.method == 'POST':
        # FIX: Added 'prefix' to separate the two forms' data
        c_form = ChildForm(request.POST, request.FILES, instance=student, prefix='child')
        g_form = GuardianForm(request.POST, request.FILES, instance=student.guardian, prefix='guardian')
        
        if c_form.is_valid() and g_form.is_valid():
            c_form.save()
            g_form.save()
            messages.success(request, 'Student details updated successfully!')
            return JsonResponse({'status': 'success'})
        else:
            # Merge errors from both forms
            errors = {**c_form.errors, **g_form.errors}
            return JsonResponse({'status': 'error', 'errors': errors})

    # FIX: Added 'prefix' here as well for the GET request
    c_form = ChildForm(instance=student, prefix='child')
    g_form = GuardianForm(instance=student.guardian, prefix='guardian')
    
    html = render_to_string('children/partials/student_edit_modal.html', {
        'student': student, 'c_form': c_form, 'g_form': g_form
    }, request=request)
    
    return JsonResponse({'html': html})

def student_delete(request, pk):
    if request.method == 'POST':
        student = get_object_or_404(Child, pk=pk)
        student.delete()
        messages.success(request, 'Student record deleted.')
        return redirect('children:all_students')

# Placeholders for other views
def student_promotion(request):
    return render(request, 'children/student_promotion.html')

def class_list(request):
    return render(request, 'children/class_list.html')