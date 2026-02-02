import os
import sys
import django

# Setup Django environment
sys.path.append('d:/nutrigem2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutrigem_backend.settings')
django.setup()

from django.contrib.auth.models import User
from django_otp import devices_for_user

users = User.objects.all()
print(f"{'Username':<20} | {'Email':<30} | {'Devices'}")
print("-" * 70)
for user in users:
    devices = list(devices_for_user(user))
    device_names = [str(d) for d in devices]
    print(f"{user.username:<20} | {user.email:<30} | {device_names}")
