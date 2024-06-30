from django.urls import path
from . import views
from hababy_app import views as hababy_views


urlpatterns = [
    path('login_usuaria/', views.login_usuaria, name='login_usuaria'),
    path('login_completado/', views.login_completado, name='login_completado'),
    path('login_incorrecto/', views.login_incorrecto, name='login_incorrecto'),
    path('logout_usuaria/', views.logout_usuaria, name='logout_usuaria'),
    path('registro/', views.registro,name="registro"),
    path('registro_completado/', views.registro_completado,name="registro_completado"),
    path('registro/verificar_codigo_para_correo/',views.verificar_codigo_para_correo,name="verificar_codigo_para_correo"),
    path('registro/braintree/', views.braintree_view, name='braintree'),
    path('registro/braintree/procesar_pago/', views.procesar_pago, name='procesar_pago'),
    path('login_usuaria/olvido_contrasenia/', views.olvido_contrasenia, name='olvido_contrasenia'),
    path('login_usuaria/olvido_contrasenia/modificar_contrasenia/', views.modificar_contrasenia, name='modificar_contrasenia'),
    path('login_usuaria/olvido_contrasenia/verificar_codigo_para_contrasenia/', views.verificar_codigo_para_contrasenia, 
         name='verificar_codigo_para_contrasenia'),
    path('registro/braintree_social/', views.braintree_social, name='braintree_social'),
    path('registro/braintree_social/procesar_pago_social/', views.procesar_pago_social, name='procesar_pago_social'),
    path('mi_perfil/',views.mi_perfil,name="mi_perfil"),
    path('mi_perfil/eliminar_mi_perfil/',views.eliminar_mi_perfil,name="eliminar_mi_perfil"),
    path('perfil_actualizado/',views.perfil_actualizado,name="perfil_actualizado"),


    

]