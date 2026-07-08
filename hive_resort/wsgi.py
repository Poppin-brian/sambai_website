"""WSGI config for the hive_resort project."""
import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hive_resort.settings")

application = get_wsgi_application()
