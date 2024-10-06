from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import LockScreen, DomainNotification
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ConnectedClient
from .models import LockScreen
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


@csrf_exempt
def receive_clients(request):
    if request.method == 'POST':
        try:
            raw_data = request.body.decode('utf-8')
            print("Raw request body:", raw_data)

            # Load the outer JSON
            data = json.loads(raw_data)
            print("Parsed outer JSON:", data)

            # The 'clients' field is still a string, so load it again as JSON
            clients_data = json.loads(data.get('clients', '[]'))
            print("Parsed clients data:", clients_data)


            
            # Flush the existing connected clients data
            ConnectedClient.objects.all().delete()
            
            # Now you can process the clients data as usual
            for client in clients_data:
                # Use .get() method to safely access keys, avoiding KeyError
                client_id = client.get('id')
                name = client.get('name', 'Unknown')
                ip_address = client.get('ip_address', '0.0.0.0')
                status = client.get('status', 'disconnected')
                systemname = client.get('systemname', 'unknown')
                OS = client.get('OS', 'unknown')
                last_domain_accessed = client.get('last_domain_accessed', 'www.google.com')
                
                # Ensure client_id is present
                if client_id:
                    ConnectedClient.objects.create(
                        client_id=client_id,
                        name=name,
                        ip_address=ip_address,
                        status=status,
                        systemname=systemname,
                        OS=OS,
                        last_domain_accessed=last_domain_accessed,
                    )
            
            return JsonResponse({'status': 'success'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid data format'}, status=400)
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

# Simulated storage (you'll likely replace this with database queries)
def display_clients(request):
    clients = ConnectedClient.objects.all()
    return render(request, 'control_panel/display_clients.html', {'clients': clients})



def delete_screen(request):
    if request.method == 'POST':
        screen_id = request.POST.get('screen_id')
        try:
            screen = LockScreen.objects.get(id=screen_id)
            screen.delete()  # Delete the selected screen
        except LockScreen.DoesNotExist:
            pass  # Handle the case where the screen doesn't exist

    return redirect('manage_lock_screens')

def set_active_screen(request):
    if request.method == 'POST':
        screen_id = request.POST.get('screen_id')
        try:
            # Deactivate all lock screens first
            LockScreen.objects.all().update(is_active=False)

            # Activate the selected lock screen
            screen = LockScreen.objects.get(id=screen_id)
            screen.is_active = True
            screen.save()

        except LockScreen.DoesNotExist:
            pass  # Handle the case where the screen doesn't exist

    return redirect('manage_lock_screens')