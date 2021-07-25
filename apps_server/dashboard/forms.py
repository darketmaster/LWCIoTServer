from datetime import datetime

from django.forms import *

#IMPORTAR MODELOS
from lwc_api.models import Device,DeviceData

class DeviceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Device
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'nonce': Textarea(
                attrs={
                    'placeholder': 'Ingrese nonce',
                    'rows': 2,
                    'cols': 2
                }
            ),
            'assoc': TextInput(
                attrs={
                    'placeholder': 'Ingrese un asociacion',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data