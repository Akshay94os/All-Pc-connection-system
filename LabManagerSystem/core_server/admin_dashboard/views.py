import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import LabComputer, CommandLog

# 1. Load the Web Dashboard
def dashboard_home(request):
    computers = LabComputer.objects.all()
    return render(request, 'dashboard.html', {'computers': computers})

# 2. API: Register a new student PC
@csrf_exempt
def register_computer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mac = data.get('mac_address')
            
            computer, created = LabComputer.objects.update_or_create(
                mac_address=mac,
                defaults={
                    'hostname': data.get('hostname'),
                    'ip_address': data.get('ip_address'),
                    'os_version': data.get('os_version'),
                    'is_online': True,
                    'last_seen': timezone.now()
                }
            )
            return JsonResponse({'status': 'success', 'message': 'Computer saved to database!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'failed', 'message': 'Only POST allowed'})

# 3. API: Save a command from the Web Dashboard
@csrf_exempt
def send_command(request, mac_address):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            command_text = data.get('command')
            
            computer = LabComputer.objects.get(mac_address=mac_address)
            
            CommandLog.objects.create(
                computer=computer,
                command=command_text,
                status='Pending'
            )
            return JsonResponse({'status': 'success', 'message': f'Command "{command_text}" queued for {computer.hostname}!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# 4. API: Give pending commands to the student PCs
@csrf_exempt
def get_pending_commands(request, mac_address):
    if request.method == 'GET':
        try:
            computer = LabComputer.objects.get(mac_address=mac_address)
            computer.last_seen = timezone.now()
            computer.is_online = True
            computer.save()

            pending_command = CommandLog.objects.filter(computer=computer, status='Pending').first()
            
            if pending_command:
                pending_command.status = 'Sent'
                pending_command.save()
                return JsonResponse({'has_command': True, 'command_id': pending_command.id, 'command': pending_command.command})
            else:
                return JsonResponse({'has_command': False})
                
        except LabComputer.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Computer not found'}, status=404)

import socket

@csrf_exempt
def wake_computer(request, mac_address):
    if request.method == 'POST':
        try:
            # 1. Clean up the MAC address (remove colons)
            mac_clean = mac_address.replace(':', '').replace('-', '')
            
            if len(mac_clean) != 12:
                return JsonResponse({'status': 'error', 'message': 'Invalid MAC format'}, status=400)

            # 2. Create the Magic Packet (6 'FF' bytes followed by the MAC address repeated 16 times)
            magic_packet = bytes.fromhex('FF' * 6 + mac_clean * 16)

            # 3. Broadcast it over the local network on port 9
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(magic_packet, ('<broadcast>', 9))
            sock.close()

            return JsonResponse({'status': 'success', 'message': f'Wake signal sent to {mac_address}!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)            

@csrf_exempt
def send_bulk_command(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mac_list = data.get('mac_addresses', [])
            command_text = data.get('command')
            
            from .models import CommandLog
            # Loop through every checked PC and give it the command
            for mac in mac_list:
                try:
                    computer = LabComputer.objects.get(mac_address=mac)
                    CommandLog.objects.create(
                        computer=computer,
                        command=command_text,
                        status='Pending'
                    )
                except LabComputer.DoesNotExist:
                    continue
                    
            return JsonResponse({'status': 'success', 'message': f'Command queued for {len(mac_list)} selected PCs!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)