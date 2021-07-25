from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import FormView,RedirectView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import login,logout
import serverIoTLWC.settings as setting
# Create your views here.


class LoginFormView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context

#VISTA LOGOUT A TRAVES DE RedirectView
class LogoutRedirectView(RedirectView):
    pattern_name = 'login'

    def dispatch(self,request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
