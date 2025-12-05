from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from children.models import Guardian  # Importing from children app
from children.forms import GuardianForm # Reusing the form to keep it DRY
from django.contrib.auth.decorators import login_required

@login_required
def guardian_list(request):
    """Renders the list of guardians with their connected children."""
    # prefetch_related is important here to avoid 85+ database queries
    guardians = Guardian.objects.prefetch_related('children').all().order_by('-id')
    
    return render(request, 'guardians/guardian_list.html', {
        'guardians': guardians,
        'total_count': guardians.count()
    })

@login_required
def guardian_detail_ajax(request, pk):
    """AJAX: Returns the Edit Modal content."""
    guardian = get_object_or_404(Guardian, pk=pk)

    if request.method == 'POST':
        form = GuardianForm(request.POST, request.FILES, instance=guardian)
        if form.is_valid():
            form.save()
            messages.success(request, f'Profile for {guardian.name} updated successfully!')
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

    form = GuardianForm(instance=guardian)
    
    html = render_to_string('guardians/partials/guardian_edit_modal.html', {
        'guardian': guardian,
        'form': form
    }, request=request)

    return JsonResponse({'html': html})

@login_required
def guardian_delete(request, pk):
    """Deletes a guardian and their connected children."""
    if request.method == 'POST':
        guardian = get_object_or_404(Guardian, pk=pk)
        name = guardian.name
        guardian.delete()
        messages.success(request, f'Guardian {name} and linked records deleted.')
        return redirect('guardians:guardian_list')