from django.contrib import admin
from machine.models import Controler_threshold,Processor_threshold,Controler,Processor
# Register your models here.

admin.site.register(Controler_threshold)
admin.site.register(Processor_threshold)
admin.site.register(Controler)
admin.site.register(Processor)