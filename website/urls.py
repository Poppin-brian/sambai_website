from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("restaurant-bar/", views.restaurant_bar, name="restaurant_bar"),
    path("events/", views.events, name="events"),
    path("gallery/", views.gallery, name="gallery"),
    path("contact/", views.contact, name="contact"),
]
