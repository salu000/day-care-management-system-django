from django.shortcuts import render

def all_students(request):
    """Renders the list view for all enrolled children."""
    return render(request, 'children/all_students.html')

def admission_form(request):
    """Renders the form page for new student admission."""
    return render(request, 'children/admission_form.html')

def student_promotion(request):
    """Renders the management page for promoting students to the next class."""
    return render(request, 'children/student_promotion.html')

def class_list(request):
    """Renders the class management page."""
    return render(request, 'children/class_list.html')