# students/middleware.py

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.middleware import get_user
from django.shortcuts import redirect

# class CustomSessionMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         request.user = get_user(request)
#         if request.user.is_authenticated:
#             if request.session.get_expiry_age() <= 0:
#                 print('not session------')
#                 # Session has expired, redirect to login-again page
#                 return redirect('/la')
#             else:
#                 print('session ddd')
#                 # Reset session expiry to 2 minutes on each request
#                 request.session.set_expiry(10)
#         else:
#             # Optional: Handle unauthenticated users differently if needed
#             pass


class CustomSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get the user from the request
        print('----dddd---',request.session.get_expiry_age())
        request.user = get_user(request)
        # Check if the user is authenticated
        if request.user.is_authenticated:
            print('User is authenticated')
            # Reset session expiry to 2 minutes (120 seconds) on each request
            request.session.set_expiry(10)
        
        # if request.sessio
        
        else:
            print('ver----',request.user.is_anonymous)
            print('User is not authenticated but session is still valid')
            




# BAAS/middleware/custom_csrf.py

# import logging
# from django.middleware.csrf import CsrfViewMiddleware

# logger = logging.getLogger(__name__)

# class CustomCsrfViewMiddleware(CsrfViewMiddleware):
#     def process_view(self, request, callback, callback_args, callback_kwargs):
#         csrf_token = request.headers.get('X-CSRFToken')
#         if csrf_token:
#             request.META['CSRF_COOKIE'] = csrf_token
#         else:
#             logger.warning("CSRF Token missing in request headers")
#         logger.debug(f"Request Path: {request.path}")
#         logger.debug(f"request headers : {request.headers}")
#         logger.debug(f"request body : {request.body}")
#         logger.debug(f"CSRF Token from request header: {request.META.get('HTTP_X_CSRFTOKEN')}")
#         logger.debug(f"CSRF Token from cookie: {request.COOKIES.get('csrftoken')}")
#         logger.debug(f"Session ID from cookie: {request.COOKIES.get('sessionid')}")
#         logger.debug(f"Request Method: {request.method}")
#         logger.debug(f"User: {request.user}")
#         return super().process_view(request, callback, callback_args, callback_kwargs)
 