from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from .forms import RegisterForm
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserProfileForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')
    
@method_decorator(login_required, name='dispatch')
class UserProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Si se proporciona user_id, muestra el perfil de ese usuario
        user_id = self.kwargs.get('user_id')
        if user_id:
            context['profile_user'] = get_object_or_404(User, id=user_id)
        else:
            # De lo contrario, muestra el perfil del usuario autenticado
            context['profile_user'] = self.request.user
            
        # En el contexto de su vista de perfil
        context['password_reset_url'] = reverse('password_reset', kwargs={'from_where': 'profile'})

        return context
    

def update_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            request.user.first_name = request.POST['first_name']
            request.user.last_name = request.POST['last_name']
            request.user.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
        
    return render(request, 'accounts/update_profile.html', {'form': form})

# En la vista de restablecimiento de contraseña
# En la vista de restablecimiento de contraseña
# En la vista de restablecimiento de contraseña
class CustomPasswordResetView(PasswordResetView):
    template_name = "accounts/registration/password_reset_form.html"
    email_template_name = "accounts/registration/password_reset_email.html"
    subject_template_name = "accounts/registration/password_reset_subject.txt"

    def dispatch(self, *args, **kwargs):
        from_where_url = self.kwargs.get('from_where', None)
        
        if from_where_url in ['profile', 'login']:
            # Si viene de 'profile' o 'login', toma 'from_where' de la URL
            self.request.session['from_where'] = from_where_url
        else:
            # En otros casos, toma 'from_where' de la variable de sesión
            from_where_session = self.request.session.get('from_where', 'login')
            self.request.session['from_where'] = from_where_session

        print("desde donde", self.request.session['from_where'])
        return super().dispatch(*args, **kwargs)



# En la vista que maneja la finalización del restablecimiento de la contraseña
def password_reset_complete_view(request):
    if 'from_where' in request.session:
        del request.session['from_where']
    # Aquí puede redirigir al usuario o mostrar una plantilla, según lo necesite
    return redirect('login')  # Redirigir al inicio de sesión como ejemplo
