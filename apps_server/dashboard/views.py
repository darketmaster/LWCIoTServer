from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.urls import reverse_lazy
#IMPORTAR VISTA GENERICAS
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,FormView

#IMPORTAR MODELOS
from lwc_api.models import Device,DeviceData

#IMPORTAR FORMULARIOS
from apps_server.dashboard.forms import DeviceForm

#LISTAR
class DeviceListView(LoginRequiredMixin,ListView):
    model = Device
    template_name = 'device/list.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Device.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Dispositivos'
        context['create_url'] = reverse_lazy('dashboard:device_create')
        context['list_url'] = reverse_lazy('dashboard:device_list')
        context['entity'] = 'Dispositivos'
        return context

#CREAR
class DeviceCreateView(LoginRequiredMixin,CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/create.html'
    success_url = reverse_lazy('dashboard:device_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de dispositivo'
        context['entity'] = 'Dispositivos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

#UPDATE
class CategoryUpdateView(LoginRequiredMixin,UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/create.html'
    success_url = reverse_lazy('dashboard:device_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición un dispositivo'
        context['entity'] = 'Dispositivos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

#DELETE
class DeviceDeleteView(LoginRequiredMixin,DeleteView):
    model = Device
    template_name = 'device/delete.html'
    success_url = reverse_lazy('dashboard:device_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un dispositivo'
        context['entity'] = 'Dispositivos'
        context['list_url'] = self.success_url
        return context

#LISTAR DATA
class DeviceDataListView(LoginRequiredMixin,ListView):
    model = DeviceData
    template_name = 'device/list_data.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                #test = DeviceData.objects.all()
                #print(test)
                for i in DeviceData.objects.all():
                    data.append(i.toJSON())
                print(data)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado data de dispositivos'
        context['create_url'] = reverse_lazy('dashboard:device_data_list')
        context['list_url'] = reverse_lazy('dashboard:device_data_list')
        context['entity'] = 'Data Dispositivos'
        return context