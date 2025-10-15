#!/usr/bin/env python
import os
import django

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qfieldcloud.settings')

# Setup Django
django.setup()

from django.contrib.auth import get_user_model

def create_superuser():
    """Create superuser if it doesn't exist"""
    User = get_user_model()

    if not User.objects.filter(username='admin').exists():
        print("Creating superuser...")
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("Superuser created successfully!")
        print("Username: admin")
        print("Password: admin123")
        print("Email: admin@example.com")
    else:
        print("Superuser 'admin' already exists.")

if __name__ == '__main__':
    create_superuser()