"""
ASGI config for MyVkFeed project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

<<<<<<< HEAD
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyVkFeed.settings')
=======
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyVkFeed.settings")
>>>>>>> dev

application = get_asgi_application()
