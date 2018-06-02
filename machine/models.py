from django.db import models

# Create your models here.
class Controler(models.Model):
    timestamp=models.DateTimeField(auto_now_add=True)
    water_in=models.FloatField(verbose_name='进水流量')
    water_out=models.FloatField(verbose_name='出水流量')
    COD=models.FloatField(verbose_name='出水COD')
    BOD=models.FloatField(verbose_name='出水BOD')

    class Meta:
        ordering=('-timestamp',)

class Controler_threshold(models.Model):
    water_in = models.FloatField(verbose_name='进水流量')
    water_out = models.FloatField(verbose_name='出水流量')
    COD = models.FloatField(verbose_name='出水COD')
    BOD = models.FloatField(verbose_name='出水BOD')

class Processor(models.Model):
    timestamp=models.DateTimeField(auto_now_add=True)
    level=models.FloatField(verbose_name='提升泵液位')
    temperature=models.FloatField(verbose_name='曝气池温度')
    PH=models.FloatField(verbose_name='曝气池PH')
    density=models.FloatField(verbose_name='污泥浓度')

    class Meta:
        ordering=('-timestamp',)

class Processor_threshold(models.Model):
    level = models.FloatField(verbose_name='提升泵液位')
    temperature_min = models.FloatField(verbose_name='最低曝气池温度')
    temperature_max = models.FloatField(verbose_name='最大曝气池温度')
    PH_min = models.FloatField(verbose_name='最低曝气池PH')
    PH_max = models.FloatField(verbose_name='最大曝气池PH')
    density_min = models.FloatField(verbose_name='最低污泥浓度')
    density_max = models.FloatField(verbose_name='最大污泥浓度')