class EnsureSecureHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is not secure
        if not request.is_secure():
            # Here, you can raise a custom exception or return a HttpResponseForbidden
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("HTTP request not allowed. Use HTTPS")
        
        return self.get_response(request)
