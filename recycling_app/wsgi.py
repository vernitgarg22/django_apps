"""
WSGI config for recycling_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application


sys.path.append("c:/cygwin64/home/kaebnickk/recycling_app")
os.environ["DJANGO_SETTINGS_MODULE"] = "recycling_app.settings"
application = get_wsgi_application()
