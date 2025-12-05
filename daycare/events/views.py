from django.shortcuts import render

# Create your views here.

def dashboard_index(request):
    return render(request, 'events/dashboard_index.html')