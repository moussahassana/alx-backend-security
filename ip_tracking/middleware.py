import requests
from django.core.cache import cache
from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        path = request.path

        # Block IP if blacklisted
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP is blocked.")

        # Try to get geo info from cache
        geo_key = f"geo:{ip}"
        geo_data = cache.get(geo_key)

        if not geo_data:
            try:
                response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    geo_data = {
                        "country": data.get("country", ""),
                        "city": data.get("city", "")
                    }
                    cache.set(geo_key, geo_data, timeout=60 * 60 * 24)  # 24 hours
                else:
                    geo_data = {"country": "", "city": ""}
            except requests.RequestException:
                geo_data = {"country": "", "city": ""}

        # Log the request
        RequestLog.objects.create(
            ip_address=ip,
            path=path,
            country=geo_data["country"],
            city=geo_data["city"]
        )

        return self.get_response(request)
