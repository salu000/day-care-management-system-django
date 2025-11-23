from django.shortcuts import render

def guardian_list(request):
    """Renders the list view for all registered guardians."""
    return render(request, 'guardians/guardian_list.html')