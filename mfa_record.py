import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutrigem_backend.settings')
django.setup()

from django.contrib.auth.models import User
from django_otp.plugins.otp_email.models import EmailDevice
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice
from django_otp import devices_for_user

def ensure_email_devices():
    for user in User.objects.all():
        # Remove TOTP and Static devices to ensure ONLY email is used
        TOTPDevice.objects.filter(user=user).delete()
        StaticDevice.objects.filter(user=user).delete()
        
        devices = list(devices_for_user(user))
        has_email = any(isinstance(d, EmailDevice) for d in devices)
        
        if not has_email and user.email:
            device = EmailDevice.objects.create(
                user=user, 
                name='default', 
                email=user.email, 
                confirmed=True
            )
            print(f"Created and confirmed email device for {user.username} ({user.email})")
        else:
            print(f"User {user.username} already has an email device or no email address.")

if __name__ == "__main__":
    ensure_email_devices()
