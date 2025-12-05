import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.template.loader import render_to_string
from .models import Child, Guardian
from .forms import ChildForm, GuardianForm
from django.contrib.auth.decorators import login_required


@login_required
def admission_form(request):
    """Handles creating a new student with either a NEW or EXISTING guardian."""
    
    # 1. Fetch all guardians for the 'Existing' dropdown
    all_guardians = Guardian.objects.all().order_by('name')

    if request.method == 'POST':
        # Determine which mode the user selected
        guardian_mode = request.POST.get('guardian_mode') # 'new' or 'existing'
        
        c_form = ChildForm(request.POST, request.FILES, prefix='child')
        
        # We initialize g_form but we might not validate it if mode is 'existing'
        g_form = GuardianForm(request.POST, request.FILES, prefix='guardian')

        if c_form.is_valid():
            child = c_form.save(commit=False)
            guardian_instance = None

            # --- LOGIC BRANCH ---
            if guardian_mode == 'existing':
                # User selected an existing parent
                existing_id = request.POST.get('existing_guardian_id')
                if not existing_id:
                    messages.error(request, "Please select a guardian from the list.")
                    return render(request, 'children/admission_form.html', {
                        'c_form': c_form, 'g_form': g_form, 'all_guardians': all_guardians
                    })
                try:
                    guardian_instance = Guardian.objects.get(id=existing_id)
                except Guardian.DoesNotExist:
                    messages.error(request, "Selected guardian does not exist.")
                    return render(request, 'children/admission_form.html', {
                        'c_form': c_form, 'g_form': g_form, 'all_guardians': all_guardians
                    })

            else:
                # User is creating a NEW parent
                if g_form.is_valid():
                    guardian_instance = g_form.save()
                else:
                    # If Child form is valid but Guardian form has errors
                    messages.error(request, "Please correct the errors in the Guardian form.")
                    return render(request, 'children/admission_form.html', {
                        'c_form': c_form, 'g_form': g_form, 'all_guardians': all_guardians
                    })

            # --- FINAL SAVE ---
            if guardian_instance:
                child.guardian = guardian_instance
                child.save()
                messages.success(request, f'Successfully enrolled {child.full_name} under guardian {guardian_instance.name}!')
                return redirect('children:all_students')
        
        else:
            messages.error(request, "Please correct the errors in the Child form.")

    else:
        # GET Request
        c_form = ChildForm(prefix='child')
        g_form = GuardianForm(prefix='guardian')

    return render(request, 'children/admission_form.html', {
        'c_form': c_form, 
        'g_form': g_form,
        'all_guardians': all_guardians
    })

@login_required
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
@login_required
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
@login_required
def student_delete(request, pk):
    if request.method == 'POST':
        student = get_object_or_404(Child, pk=pk)
        student.delete()
        messages.success(request, 'Student record deleted.')
        return redirect('children:all_students')

# Placeholders for other views
@login_required
def student_promotion(request):
    return render(request, 'children/student_promotion.html')

@login_required
def class_list(request):
    return render(request, 'children/class_list.html')