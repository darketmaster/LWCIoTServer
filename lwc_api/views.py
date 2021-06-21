from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from .serializers import DeviceSerializer
from .models import Device
import datetime
import hashlib
import json
import base64
from django.core.exceptions import ObjectDoesNotExist
from .pyascon.ascon import ascon_decrypt

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
                  return Response(dic)
            else:
                return Response('{"error":"Unauthorized access"}',status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response('{"error":"Bad Request"}',status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def setDataDevice(request):
    """
    Set data.
    """
    print(request.data)
    if request.method == 'POST':  
        if "device" in request.data and "data" in request.data : 
            device = request.data["device"]
            data = request.data["data"] 
            print(request.data)

            try:
                objdevice = Device.objects.get(name=device)
                nonce = objdevice.nonce
                assoc = objdevice.assoc                
            except ObjectDoesNotExist:
                return Response('{"error":"Unauthorized access"}',status=status.HTTP_401_UNAUTHORIZED)

            key = "IOT_APP_LWC_ASCON_SECRET_KEY---#";
            decode = base64.b64decode(data)
            decript = ascon_decrypt(key, nonce, assoc, decode)

            return Response(assoc + " " + nonce + " " + data)

        else:
            return Response('{"error":"Bad Request"}',status=status.HTTP_400_BAD_REQUEST)

