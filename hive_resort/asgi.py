"""ASGI config for the hive_resort project."""
import os

from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hive_resort.settings")

application = get_asgi_application()
