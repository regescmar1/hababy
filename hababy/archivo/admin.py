from django.contrib import admin

# Register your models here.

from .models import ArchivoCurvaLarga, ArchivoExtracciones, ArchivoObstetra

admin.site.register(ArchivoExtracciones)
admin.site.register(ArchivoObstetra)
admin.site.register(ArchivoCurvaLarga)