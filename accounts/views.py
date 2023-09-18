from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegisterForm
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserProfileForm
from .models import UserProfile
from django.contrib.auth.models import User

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