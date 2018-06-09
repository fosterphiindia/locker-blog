"""
WSGI config for mySite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import signal

import sys
import traceback

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mySite.settings")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)