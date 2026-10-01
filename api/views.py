from django.http import JsonResponse
import os


def home(request):
    server_id = os.environ.get("SERVER_ID", "unknown")

    return JsonResponse({
        "message": "Hello from Django",
        "server": server_id
    })


def health(request):
    return JsonResponse({
        "status": "ok"
    })