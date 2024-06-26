from django.urls import path
from . import views


urlpatterns = [
    path('',views.archivo,name='archivo'),
    path('archivo_guardado_con_exito/',views.archivo_guardado_con_exito,name='archivo_guardado_con_exito'),
    path('descargar/<int:archivo_id>/', views.descargar_archivo, name='descargar_archivo'),
    path('<int:archivo_id>/', views.ver_archivo, name='ver_archivo'),
    path('eliminar/<int:archivo_id>/', views.eliminar_archivo, name='eliminar_archivo'),
    path('archivo_eliminado/',views.archivo_eliminado,name='archivo_eliminado'),
    path('generar_pdf/',views.generar_pdf,name='generar_pdf'),
]