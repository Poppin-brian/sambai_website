import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hive_resort.settings")
import django

django.setup()
from django.test import Client
from django.urls import reverse

client = Client(HTTP_HOST="localhost")
response = client.get(reverse("home"))
html = response.content.decode("utf-8")
print(response.status_code)
print("Work With Us" in html)
print("No Current Vacancies" in html)
print('aria-disabled="true"' in html)
