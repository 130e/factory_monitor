from rest_framework  import serializers
from machine.models import Controler,Controler_threshold,Processor,Processor_threshold

class ControlerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Controler
        fields=('timestamp','water_in','water_out','COD','BOD')

class Controler_thresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model=Controler_threshold
        fields=('water_in','water_out','COD','BOD')

class ProcessorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Processor
        fields=('timestamp','level','temperature','PH','density')

class Processor_thresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model=Processor_threshold
        fields=('level','temperature_min','temperature_max','PH_min','PH_max','density_min','density_max')