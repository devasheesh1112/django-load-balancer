
import logging
import time
import os

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("django.request_monitor")


class RequestMonitoringMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.perf_counter()

    def process_response(self, request, response):
        start_time = getattr(request, "start_time", None)

        if start_time is not None:
            duration_ms = (time.perf_counter() - start_time) * 1000
            server_id = os.environ.get("SERVER_ID", "unknown")

            logger.info(
                "server=%s method=%s path=%s status=%s duration_ms=%.2f",
                server_id,
                request.method,
                request.path,
                response.status_code,
                duration_ms,
            )

            response["X-Server-ID"] = server_id
            response["X-Response-Time-ms"] = f"{duration_ms:.2f}"

        return response
