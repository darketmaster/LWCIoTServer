from django.urls import path
from login.views import *
urlpatterns = [
    #path('',LoginFormsView.as_view(),name='login'),
    path('',LoginFormView.as_view(),name='login'),
    #CERRAR SESSION LOGOUT A TRAVES DE LA CLASE LogoutView
    path('logout/',LogoutView.as_view(),name='logout'),
    #CERRAR SESSUIB LOGOUT A TRAVES DE REDIRECT
    #path('logout/',LogoutRedirectView.as_view(),name='logout'),
]
