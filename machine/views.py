from django.shortcuts import render,redirect
from rest_framework import viewsets,generics
from machine.models import Controler,Processor,Controler_threshold,Processor_threshold
from machine.serializers import ControlerSerializer,ProcessorSerializer
from rest_framework import permissions
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.response import Response
#from django.contrib.auth.models import User
from users.models import User
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

class ControlerViewSet(viewsets.ModelViewSet):
    queryset = Controler.objects.all()
    serializer_class = ControlerSerializer
    #permission_classes = (permissions.IsAuthenticated,permissions.DjangoModelPermissions)
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
    #permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ControlerSerializer
    def get_queryset(self):
        try:
            year=int(self.request.query_params.get('year',None)) #query_params
            month=int(self.request.GET.get('month',None))
            day=int(self.request.GET.get('day',None))
            return Controler.objects.filter(timestamp__date=datetime.date(year,month,day))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        header = {'Access-Control-Allow-Origin': '*'}
        #page = self.paginate_queryset(queryset)
        #if page is not None:
        #    serializer = self.get_serializer(page, many=True)
        #    return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data,headers=header)

@api_view(['GET'])
#@permission_classes((permissions.IsAuthenticated,))
def Controler_latest(request,format=None):
    header={'Access-Control-Allow-Origin':'*'}
    try:
        data=Controler.objects.latest('timestamp')
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer=ControlerSerializer(data)
    return Response(serializer.data,headers=header)


###############################  Processor  #############################################

class ProcessorViewSet(viewsets.ModelViewSet):
    queryset = Processor.objects.all()
    serializer_class = ProcessorSerializer
    #permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        threshold=Processor_threshold.objects.get(pk=1)
        message=[]
        if serializer.validated_data['level']>threshold.level:
            message+=['污水处理器：提升泵液位{},超出阈值.'.format(serializer.validated_data['level'])]
        if threshold.temperature_max>serializer.validated_data['temperature']>threshold.temperature_min:
            message+=['污水处理器：曝气池温度{},超出阈值.'.format(serializer.validated_data['temperature'])]
        if threshold.PH_max>serializer.validated_data['PH']>threshold.PH_min:
            message+=['污水处理器：曝气池PH{}，超出阈值.'.format(serializer.validated_data['PH'])]
        if threshold.density_max>serializer.validated_data['density']>threshold.density_min:
            message+=['污水处理器：污泥浓度{}，超出阈值.'.format(serializer.validated_data['density'])]
        if len(message)!=0:
            send_to=[user.email for user in User.objects.filter(groups__name='administrator')]
            send_mail('污水处理器异常警告',
                      '\n'.join(message),
                      'cjt1256182832@aliyun.com',
                      send_to,
                      fail_silently=False
                      )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ProcessorList(generics.ListAPIView):
    serializer_class = ProcessorSerializer
    def get_queryset(self):
        try:
            year=int(self.request.GET.get('year',None))
            month=int(self.request.GET.get('month',None))
            day=int(self.request.GET.get('day',None))
            return Processor.objects.filter(timestamp__date=datetime.date(year,month,day))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        header = {'Access-Control-Allow-Origin': '*'}
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data,headers=header)

@api_view(['GET'])
def Processor_latest(request,format=None):
    header = {'Access-Control-Allow-Origin': '*'}
    try:
        data=Processor.objects.latest('timestamp')
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer=ProcessorSerializer(data)
    return Response(serializer.data,headers=header)

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def ControlerDetail(request):
    return render(request,'Detail-re.html')


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def ProcessorDetail(request):
    return render(request,'ProcessorDetail.html')

@csrf_exempt
def Search(request):
    machine=request.POST.get('machine')
    print(machine)
    machine
    if machine=='controler':
        return redirect('/api/machine/detail/controler/')
    if machine=='processor':
        return redirect('/api/machine/detail/processor/')
    return render()

