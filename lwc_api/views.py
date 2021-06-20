from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
from rest_framework import viewsets

from .serializers import DeviceSerializer
from .models import Device
import datetime
import hashlib
import json 

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all().order_by('name')
    serializer_class = DeviceSerializer

@api_view(['POST'])
def registerDevice(request):
    """
    Register a new Device for send nonce.
    """
    print(request.data)
    if request.method == 'POST':  
        if "device" in request.data and "key" in request.data and "assoc" in request.data : 
            device = request.data["device"]
            key = request.data["key"] 
            assoc = request.data["assoc"]
            print(request.data)
            if key == 'IOT-Key-202107lwc':
                  now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                  cad = now+'#'+device
                  nonce = hashlib.md5(cad.encode()).hexdigest()
                  dic = {
                      "nonce": nonce,
                      #"cad": cad,
                  }
                  model, bcreated = Device.objects.get_or_create(name=device)
                  model.nonce = nonce
                  model.assoc = assoc
                  model.save()
                  print(device + " Created: " + ("True" if bcreated else "False"))
                  return Response(json.dumps(dic))
            else:
                return Response('{"error":"Unauthorized access"}',status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response('{"error":"Bad sRequest"}',status=status.HTTP_400_BAD_REQUEST)
