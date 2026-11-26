from django.http import JsonResponse
from django.urls import path


def home(request):
    return JsonResponse({"message": "Hello, world!", "app": "Fito"})


def health(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("", home, name="home"),
    path("health/", health, name="health"),
]
