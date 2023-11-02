from django.shortcuts import redirect
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            # Aquí puedes excluir algunas URL públicas si es necesario
            if request.path not in ['/', '/register/']:
                return redirect(settings.LOGIN_URL)
        response = self.get_response(request)
        return response