from django.shortcuts import render

def billing_view(request):
    """Renders the main payments and billing management view."""
    return render(request, 'billings/billing_view.html')