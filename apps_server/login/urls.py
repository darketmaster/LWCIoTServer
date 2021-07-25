from django.urls import path
from apps_server.login.views import *
urlpatterns = [
    path('',LoginFormView.as_view(),name='login'),
    #CERRAR SESSION LOGOUT A TRAVES DE LA CLASE LogoutView
    path('logout/',LogoutView.as_view(),name='logout'),
]
