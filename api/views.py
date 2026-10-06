from django.http import JsonResponse
import os


def home(request):
    server_id = os.environ.get("SERVER_ID", "unknown")

    return JsonResponse({
        "message": "Hello from Django",
        "server": server_id
    })


def health_check(request):
    server_id = os.environ.get("SERVER_ID", "unknown")

    return JsonResponse({
        "status": "healthy",
        "server": server_id
    })


def server_info(request):
    server_id = os.environ.get("SERVER_ID", "unknown")

    return JsonResponse({
        "service": "django-load-balancer",
        "server": server_id,
        "status": "running"
    })