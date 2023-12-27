"""
WSGI config for azureproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""


import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'azureproject.settings')

application = get_wsgi_application()

# Apply Whitenoise to serve static files
from whitenoise import WhiteNoise
application = get_wsgi_application()
application = WhiteNoise(application)

# Add staticfiles entry to the Python path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))