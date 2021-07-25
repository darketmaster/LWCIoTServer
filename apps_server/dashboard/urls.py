from django.urls import path
from apps_server.dashboard.views import *
#DEFINICION MAS ESPECIFICA
app_name = 'dashboard'
urlpatterns = [
    path('', DeviceListView.as_view(), name='device_list'),
    #DEVICE
    path('device/add/', DeviceCreateView.as_view(), name='device_create'),
    path('device/update/<int:pk>/', CategoryUpdateView.as_view(), name='device_update'),
    path('device/delete/<int:pk>/', DeviceDeleteView.as_view(), name='device_delete'),
    #DATA DEVICE
    path('device/data/', DeviceDataListView.as_view(), name='device_data_list'),
]