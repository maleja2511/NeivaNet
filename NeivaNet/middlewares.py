from django.shortcuts import redirect
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            # Aquí puedes excluir algunas URL públicas si es necesario
            public_urls = [
                '/', 
                '/register/', 
                '/password_reset/login/',
                '/password_reset/profile/',
                '/password_reset/done/', 
                '/reset/',  # Esta ruta es un poco complicada porque tiene parámetros dinámicos
                '/reset/done/'
            ]
            if not any([request.path.startswith(url) for url in public_urls]):
                return redirect(settings.LOGIN_URL)
        response = self.get_response(request)
        return response
