"""
WSGI config for oauthvk project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/users/m/marselabdullin/oauthvk')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oauthvk.settings')

application = get_wsgi_application()
