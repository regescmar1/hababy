"""
URL configuration for hababy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from hababy_app import views as hababy_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', hababy_views.principal,name="principal"),
    path('acerca_de/', hababy_views.acerca_de,name="acerca_de"),
    path('contacto/', hababy_views.contacto,name="contacto"),
    path('politica_privacidad/', hababy_views.politica_privacidad,name="politica_privacidad"),

    path('oauth/', include('social_django.urls', namespace='social')),
    path('autenticacion/', include('autenticacion.urls')),

    path('educacion_maternal/',include('educacion_maternal.urls')),

    path('consejos/',include('consejos.urls')),

    path('gestion_citas/',include('gestion_citas.urls')),

    path('gestion_citas/citas_primer/odontologia/',include('odontologia.urls')),

    path('gestion_citas/citas_primer/matrona/', include('matrona.urls')),
    path('gestion_citas/citas_segundo/matrona/', include('matrona.urls')),
    path('gestion_citas/citas_tercer/matrona/', include('matrona.urls')),

    path('gestion_citas/citas_primer/obstetra/', include('obstetra.urls')),
    path('gestion_citas/citas_segundo/obstetra/', include('obstetra.urls')),
    path('gestion_citas/citas_tercer/obstetra/', include('obstetra.urls')),

    path('gestion_citas/citas_primer/obstetra/archivos/',include('archivo.urls')),
    path('gestion_citas/citas_segundo/obstetra/archivos/',include('archivo.urls')),
    path('gestion_citas/citas_tercer/obstetra/uno/archivos/',include('archivo.urls')),
    path('gestion_citas/citas_tercer/obstetra/dos/archivos/',include('archivo.urls')),
    path('gestion_citas/citas_tercer/obstetra/tres/archivos/',include('archivo.urls')),
    
    path('vacunas/',include('vacuna.urls')),

    path('gestion_citas/citas_primer/extracciones/',include('extracciones.urls')),
    path('gestion_citas/citas_segundo/extracciones/',include('extracciones.urls')),
    path('gestion_citas/citas_tercer/extracciones/',include('extracciones.urls')),
    
    path('gestion_citas/citas_primer/extracciones/archivos/',include('archivo.urls')),
    path('gestion_citas/citas_segundo/extracciones/archivos/',include('archivo.urls')),
    path('gestion_citas/citas_tercer/extracciones/archivos/',include('archivo.urls')),

    path('gestion_citas/citas_segundo/extracciones/test_o_sullivan_curva_larga/archivos/',include('archivo.urls')),
    path('gestion_citas/citas_segundo/extracciones/test_o_sullivan_curva_larga/archivos/{{archivo.id}}',include('archivo.urls')),
    path('gestion_citas/citas_segundo/extracciones/test_o_sullivan_curva_larga/archivos/descargar/{{archivo.id}}',include('archivo.urls')),
    path('gestion_citas/citas_segundo/extracciones/test_o_sullivan_curva_larga/archivos/eliminar/{{archivo.id}}',include('archivo.urls')),
    path('gestion_citas/citas_segundo/extracciones/test_o_sullivan_curva_larga/archivos/generar_pdf/',include('archivo.urls')),

    path('gestion_citas/citas_primer/medicina_familia/',include('medicina_familia.urls')),
    path('gestion_citas/citas_segundo/medicina_familia/',include('medicina_familia.urls')),
    path('gestion_citas/citas_tercer/medicina_familia/',include('medicina_familia.urls')),

    path('proxima_cita/',include('proxima_cita.urls')),

    path('administrador/',include('administrador.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)