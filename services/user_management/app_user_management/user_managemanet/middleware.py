from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser
from rest_framework.response import Response
from django.shortcuts import redirect
# probleme de si suprime coki l user reste true dans data base

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def __call__(self, request):
        print("/*/*/*/*/*/*Midlwere is HERE !!!! ")
        if request.path !=  "/signup/":
            token = request.COOKIES.get('jwt')
            if token:
                try:
                    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                    request.id =  payload.get('id')
                    request.user = CustomUser.objects.get(id=request.id)
                    if request.user.is_logged_2fa  and request.path != "/login/" and request.path != '/otp/': #add Home
                        return redirect('otp')
                except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, CustomUser.DoesNotExist) as e:
                    print(f"exception ===>>  {e}")
                    request.user = AnonymousUser()
            else:
                print("Token----------->is invalid")
                request.user = AnonymousUser()            
        response = self.get_response(request)
        print(f"reponse ========= >>>>> {request}")
        return response
        
class DisableCSRF(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

# from django.http import HttpResponseForbidden
# from django.http import HttpResponseForbidden
# return HttpResponseForbidden("Accès interdit")
        
        
