"""
WSGI config for django_apps project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application


sys.path.append("c:/cygwin64/home/kaebnickk/django_apps")
os.environ["DJANGO_SETTINGS_MODULE"] = "django_apps.settings"
application = get_wsgi_application()
