from django.http import JsonResponse
from django.urls import path

from landing import views


def health(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("", views.home, name="home"),
    path("join/", views.signup, name="signup"),
    path("manifest.webmanifest", views.manifest, name="manifest"),
    path("sw.js", views.service_worker, name="service_worker"),
    path("health/", health, name="health"),
]
