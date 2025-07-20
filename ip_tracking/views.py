from django.http import JsonResponse, HttpResponse
from django_ratelimit.core import is_ratelimited


def sensitive_view(request):
    # Define rate: 10 req/min if authenticated, 5 req/min if anonymous
    limit = '10/m' if request.user.is_authenticated else '5/m'
    key = 'user_or_ip'

    # Check if request exceeds limit
    limited = is_ratelimited(
        request=request,
        key=key,
        rate=limit,
        method='GET',
        increment=True,
    )

    if limited:
        return HttpResponse("Rate limit exceeded", status=429)

    return JsonResponse({"message": "OK"})
