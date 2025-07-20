from django.http import JsonResponse, HttpResponseTooManyRequests
from ratelimit.core import is_ratelimited

def sensitive_view(request):
    # Apply different limits for authenticated vs anonymous
    limit = '10/m' if request.user.is_authenticated else '5/m'
    key = 'user_or_ip'

    # Check if limit exceeded
    limited = is_ratelimited(
        request=request,
        group=None,
        fn=None,
        key=key,
        rate=limit,
        method='GET',
        increment=True
    )

    if limited:
        return HttpResponseTooManyRequests("Rate limit exceeded")

    return JsonResponse({"message": "OK"})
