import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tapin.settings')

import django
django.setup()


from gaz.models import User



User.objects.get_or_create(
    username=os.environ.get('SUPER_USER_NAME'),
    email=os.environ.get('SUPER_USER_EMAIL'),
    password=os.environ.get('SUPER_USER_PASSWORD'),
    role='Admin',
    is_superuser=True,
    is_staff=True
)
