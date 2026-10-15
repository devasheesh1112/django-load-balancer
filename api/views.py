
from django.http import JsonResponse
import os
from itertools import count
from threading import Lock

server_id = os.environ.get("SERVER_ID", "unknown")

_request_count = count(1)
_request_lock = Lock()
requests_handled = 0


def home(request):
    global requests_handled

    with _request_lock:
        requests_handled += 1
        current_count = requests_handled

    return JsonResponse({
        "message": "Hello from Django",
        "server": server_id,
        "request_number": current_count
    })


def health_check(request):
    return JsonResponse({
        "status": "healthy",
        "server": server_id
    })


def server_info(request):
    return JsonResponse({
        "service": "django-load-balancer",
        "server": server_id,
        "status": "running",
        "requests_handled": requests_handled
    })
