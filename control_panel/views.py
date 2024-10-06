from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import LockScreen, DomainNotification
from django.core.files.storage import FileSystemStorage

# Dashboard view (optional)
def dashboard(request):
    return render(request, 'control_panel/dashboard.html')

# View to upload lock screen images
def upload_logo(request):
    if request.method == 'POST' and request.FILES['logo']:
        # Handle file upload
        logo = request.FILES['logo']
        fs = FileSystemStorage()
        filename = fs.save(logo.name, logo)
        
        # Save the lock screen in the database
        new_screen = LockScreen(logo=filename)
        new_screen.save()
        return redirect('manage_lock_screens')
    return render(request, 'control_panel/upload.html')

# View to manage lock screens
def manage_lock_screens(request):
    # List all lock screens
    lock_screens = LockScreen.objects.all()
    
    # Handle setting one as active
    if request.method == 'POST':
        screen_id = request.POST.get('screen_id')
        LockScreen.objects.update(is_active=False)  # Deactivate all
        selected_screen = LockScreen.objects.get(id=screen_id)
        selected_screen.is_active = True
        selected_screen.save()
        return redirect('manage_lock_screens')
    
    return render(request, 'control_panel/manage.html', {'lock_screens': lock_screens})

# API to get the currently active lock screen
def get_active_lock_screen(request):
    selected_screen = LockScreen.objects.filter(is_active=True).first()
    if selected_screen:
        # Build the full URL for the logo
        logo_url = request.build_absolute_uri(selected_screen.logo.url)
        return JsonResponse({'logo_url': logo_url})
    else:
        return JsonResponse({'error': 'No active lock screen found'}, status=404)

# View to manage domain notifications
def manage_domains(request):
    if request.method == 'POST':
        # Add new domain
        domain_name = request.POST.get('domain_name')
        if domain_name:
            DomainNotification.objects.create(domain=domain_name)
        # Optionally handle deleting domains
        if 'delete' in request.POST:
            domain_id = request.POST.get('domain_id')
            DomainNotification.objects.get(id=domain_id).delete()
        return redirect('manage_domains')

    # Get all domains
    domains = DomainNotification.objects.all()
    return render(request, 'control_panel/domains.html', {'domains': domains})
