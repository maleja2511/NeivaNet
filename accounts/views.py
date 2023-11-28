from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView
from .forms import RegisterForm, UserProfileForm
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

class CustomLoginView(AuthLoginView):
    def form_valid(self, form):
        # Llama al comportamiento original de form_valid
        response = super().form_valid(form)
        
        # Verifica si el usuario seleccionó "login_as_admin"
        login_as_admin = self.request.POST.get('login_as_admin', False)

        if login_as_admin:
            if self.request.user.is_staff:  # verifica si el usuario tiene permisos de administrador
                return redirect(reverse('admin:index'))  # Redirige a la consola de administración
            else:
                # Si no tiene permisos de administrador
                messages.error(self.request, "No puedes iniciar sesión como administrador.")
                return redirect(reverse('login'))
        return response

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # No activar el usuario hasta que confirme el correo
        user.save()
        profile = UserProfile.objects.create(user=user)

        # Enviar correo electrónico de confirmación
        confirmation_link = self.request.build_absolute_uri(
            reverse('confirm_email', args=[profile.confirmation_token])
        )
        subject = 'Confirmación de Registro'
        from_email = settings.DEFAULT_FROM_EMAIL
        to = user.email
        text_content = 'Por favor, confirma tu registro haciendo clic en el siguiente enlace.'
        html_content = render_to_string('accounts/confirmation_email.html', {
            'confirmation_link': confirmation_link
        })

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return super(RegisterView, self).form_valid(form)

def confirm_email(request, token):
    try:
        profile = UserProfile.objects.get(confirmation_token=token)
        if profile.confirmation_token_expired():
            context = {'message': 'El enlace de confirmación ha expirado.'}
            return render(request, 'accounts/email_confirmation.html', context)
        else:
            profile.user.is_active = True
            profile.user.save()
            context = {'message': 'Tu correo electrónico ha sido confirmado exitosamente.'}
            return render(request, 'accounts/email_confirmation.html', context)
    except UserProfile.DoesNotExist:
        context = {'message': 'Enlace de confirmación inválido.'}
        return render(request, 'accounts/email_confirmation.html', context)
    
class UserProfileView(LoginRequiredMixin, TemplateView):
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
    
@login_required
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
            
        return super().dispatch(*args, **kwargs)


# En la vista que maneja la finalización del restablecimiento de la contraseña
def password_reset_complete_view(request):
    if 'from_where' in request.session:
        del request.session['from_where']
    # Aquí puede redirigir al usuario o mostrar una plantilla, según lo necesite
    return redirect('login')  # Redirigir al inicio de sesión como ejemplo