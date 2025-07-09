# employee/middleware.py
import json
import logging
from django.utils.encoding import force_str

logger = logging.getLogger('django.request')

class RequestResponseLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.log_request(request)
        response = self.get_response(request)
        self.log_response(response)
        return response

    def log_request(self, request):
        try:
            body = self.get_request_body(request)
            request_data = {
                "method": request.method,
                "path": request.path,
                "headers": {k: v for k, v in request.headers.items()},
                "GET_params": dict(request.GET),
                "POST_params": dict(request.POST),
                "body": body,
            }
            logger.info("Incoming Request:\n%s", 
                      json.dumps(request_data, 
                                indent=2, 
                                ensure_ascii=False,  # Важно для кириллицы
                                default=str))
        except Exception as e:
            logger.error("Failed to log request: %s", str(e))

    def get_request_body(self, request):
        if not request.body:
            return None
        
        content_type = request.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            try:
                return json.loads(request.body.decode('utf-8'))
            except (UnicodeDecodeError, json.JSONDecodeError):
                return force_str(request.body)
        return force_str(request.body)

    def log_response(self, response):
        try:
            content = self.get_response_content(response)
            response_data = {
                "status": response.status_code,
                "headers": dict(response.headers),
                "content": content,
            }
            logger.info("Outgoing Response:\n%s", 
                       json.dumps(response_data, 
                                 indent=2, 
                                 ensure_ascii=False,
                                 default=str))
        except Exception as e:
            logger.error("Failed to log response: %s", str(e))

    def get_response_content(self, response):
        if not response.content:
            return None
        
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            try:
                return json.loads(response.content.decode('utf-8'))
            except (UnicodeDecodeError, json.JSONDecodeError):
                return force_str(response.content)
        return force_str(response.content)