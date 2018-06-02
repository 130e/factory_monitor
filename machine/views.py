from django.shortcuts import render
from rest_framework import viewsets,generics
from machine.models import Controler,Processor,Controler_threshold,Processor_threshold
from machine.serializers import ControlerSerializer,ProcessorSerializer
from rest_framework import permissions
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.mail import send_mail

class ControlerViewSet(viewsets.ModelViewSet):
    queryset = Controler.objects.all()
    serializer_class = ControlerSerializer
    permission_classes = (permissions.IsAuthenticated,permissions.DjangoModelPermissions)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        threshold=Controler_threshold.objects.get(pk=1)
        message=[]
        if serializer.validated_data['water_in']>threshold.water_in:
            message+=['污水进出控制器：进水流量为{},超出阈值.'.format(serializer.validated_data['water_in'])]
        if serializer.validated_data['water_out']>threshold.water_out:
            message+=['污水进出控制器：出水流量为{},超出阈值.'.format(serializer.validated_data['water_out'])]
        if serializer.validated_data['COD']>threshold.COD:
            message+=['污水进出控制器：出水COD为{}，超出阈值.'.format(serializer.validated_data['COD'])]
        if serializer.validated_data['BOD']>threshold.BOD:
            message+=['污水进出控制器：出水BOD为{}，超出阈值.'.format(serializer.validated_data['BOD'])]
        if len(message)!=0:
            send_to=[user.email for user in User.objects.filter(groups__name='administrator')]
            send_mail('污水进出控制器异常警告',
                      '\n'.join(message),
                      'cjt1256182832@aliyun.com',
                      send_to,
                      fail_silently=False
                      )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ControlerList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ControlerSerializer
    def get_queryset(self):
        try:
            year=int(self.request.query_params.get('year',None))
            month=int(self.request.query_params.get('month',None))
            day=int(self.request.query_params.get('day',None))
            return Controler.objects.filter(timestamp__date=datetime.date(year,month,day))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def Controler_latest(request,format=None):
    try:
        data=Controler.objects.latest('timestamp')
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer=ControlerSerializer(data)
    return Response(serializer.data)


###############################  Processor  #############################################

class ProcessorViewSet(viewsets.ModelViewSet):
    queryset = Processor.objects.all()
    serializer_class = ProcessorSerializer
    #authentication_classes = (SessionAuthentication,BasicAuthentication)
    #permission_classes = (permissions.IsAuthenticated,)


class ProcessorList(generics.ListAPIView):
    serializer_class = ProcessorSerializer
    def get_queryset(self):
        try:
            year=int(self.request.query_params.get('year',None))
            month=int(self.request.query_params.get('month',None))
            day=int(self.request.query_params.get('day',None))
            return Processor.objects.filter(timestamp__date=datetime.date(year,month,day))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def Processor_latest(request,format=None):
    try:
        data=Processor.objects.latest('timestamp')
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer=ProcessorSerializer(data)
    return Response(serializer.data)