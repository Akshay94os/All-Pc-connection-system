import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import LabComputer
from django.shortcuts import render
from .models import LabComputer

# --- ADD THIS NEW FUNCTION ---
def dashboard_home(request):
    # Grab all computers from the database
    computers = LabComputer.objects.all()
    # Send them to an HTML file named 'dashboard.html'
    return render(request, 'dashboard.html', {'computers': computers})
@csrf_exempt
def register_computer(request):
    if request.method == 'POST':
        try:
            # Catch the data sent by the student PC
            data = json.loads(request.body)
            mac = data.get('mac_address')
            
            # Save it to the database (or update it if it already exists)
            computer, created = LabComputer.objects.update_or_create(
                mac_address=mac,
                defaults={
                    'hostname': data.get('hostname'),
                    'ip_address': data.get('ip_address'),
                    'os_version': data.get('os_version'),
                    'is_online': True
                }
            )
            return JsonResponse({'status': 'success', 'message': 'Computer saved to database!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return JsonResponse({'status': 'failed', 'message': 'Only POST requests allowed'})