import time
from django.utils.deprecation import MiddlewareMixin
from .models import RequestLog

class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log all HTTP requests for analytics
    """
    
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        # Calculate response time
        if hasattr(request, 'start_time'):
            response_time = (time.time() - request.start_time) * 1000  # Convert to milliseconds
        else:
            response_time = 0
        
        # Get client IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        
        # Create log entry
        try:
            RequestLog.objects.create(
                method=request.method,
                path=request.path,
                status_code=response.status_code,
                response_time=response_time,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                ip_address=ip_address,
                user=request.user if request.user.is_authenticated else None,
                referrer=request.META.get('HTTP_REFERER', ''),
            )
        except Exception as e:
            # Don't let logging errors break the application
            print(f"Logging error: {e}")
        
        return response