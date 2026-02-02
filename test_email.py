import os
import django
from django.core.mail import send_mail
from django.conf import settings

# Setup Django environment
import sys
sys.path.append('d:/nutrigem2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutrigem_backend.settings')
django.setup()

try:
    print(f"Testing email to {settings.EMAIL_HOST_USER}...")
    send_mail(
        'NutriGem Test Email',
        'If you see this, email is working.',
        settings.DEFAULT_FROM_EMAIL,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
