from django.contrib import admin
from .models import *

# Configuracion extra
class PageAdmin(admin.ModelAdmin):
    search_fields = ('titulo', 'contenido')
    
# Register your models here.
admin.site.register(Page, PageAdmin)

#Configuración del panel
title = "Panel de gestión"
subtitle = "Panel de gestión"

admin.site.site_header = title
admin.site.site_title = title
admin.site.index_title = subtitle