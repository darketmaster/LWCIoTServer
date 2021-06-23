from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from .serializers import DeviceSerializer
from .models import Device, DeviceData
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
            #print(type(data))

            if type(data) != type(''):
                return Response('{"error":"Bad Request"}',status=status.HTTP_400_BAD_REQUEST)

            try:
                objdevice = Device.objects.get(name=device)
                nonce = objdevice.nonce
                assoc = objdevice.assoc.encode()                
            except ObjectDoesNotExist:
                return Response('{"error":"Not Found"}',status=status.HTTP_404_NOT_FOUND)

            key = "IOT_LWC_ASCON---"
            bkey = bytearray()
            bkey.extend(map(ord, key))            
            decode = base64.b64decode(data)
            bnonce = bytes.fromhex(nonce)
            print(len(bkey))
            #print(bnonce)
            print(len(bnonce))
            #print(decode)
            #print(assoc)
            decrypt = ascon_decrypt(bkey, bnonce, assoc, decode)
            #print(type(assoc.decode()))
            #print(type(nonce))
            #print(type(data))
            ddecrypt = decrypt.decode()
            print(ddecrypt)
            decryp_data = json.loads(ddecrypt)
            #ARRAY |    CO   |  Alcohol |   CO2  |  Tolueno  |  NH4  |  Acteona  |
            print(decryp_data['sensor'])

            import pytz
            col = pytz.timezone("America/Bogota")
            d = datetime.datetime.strptime(decryp_data["time"], '%Y-%m-%d %H:%M:%S')
            newdate = col.localize(d)
            print(d)
            print(newdate)

            model = DeviceData.objects.create(ip=decryp_data["IP"],mac=decryp_data["MAC"],ordate=newdate)
            model.mq135 = decryp_data['sensor']["MQ-135"]
            model.save()

            return Response('{"info":"Data Accepted"}')
        else:
            return Response('{"error":"Bad Request"}',status=status.HTTP_400_BAD_REQUEST)

