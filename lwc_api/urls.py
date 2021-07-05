from django.urls import include, path
from rest_framework import routers
from . import views
from django.contrib import admin

admin.site.site_header = "Ambiental Quality LWC IoT Admin"
admin.site.site_title = "Ambiental Quality LWC IoT  Admin Portal"
admin.site.index_title = "Welcome to Ambiental Quality LWC IoT Portal"

router = routers.DefaultRouter()
router.register(r'devices', views.DeviceViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', views.registerDevice),
    path('setDataDevice/', views.setDataDevice),
]