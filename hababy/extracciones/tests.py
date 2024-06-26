from django.test import TestCase

# Create your tests here.
import datetime
from django.test import Client, TestCase
from extracciones.models import CitaExtracciones
from django.contrib.auth.models import User
from django.utils import timezone

from extracciones.forms.forms import CitaExtraccionesForm

class ExtraccionesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.cita = CitaExtracciones.objects.create(
            usuaria=self.user,
            fecha=timezone.make_aware(datetime.datetime(2024, 3, 25, 8, 0, 0), timezone=timezone.get_current_timezone()),  
            analisis_normal=False,
            test_o_sullivan_positivo=False,
            rh_negativo=True,
            observaciones='Ninguna',
            trimestre=2
        )

    def test_crear_cita(self):
        cita = CitaExtracciones.objects.get(id=self.cita.id)
        expected_fecha = timezone.make_aware(datetime.datetime(2024, 3, 25, 8, 0, 0), timezone=timezone.get_current_timezone())  
        self.assertEqual(cita.fecha, expected_fecha)
        self.assertEqual(cita.usuaria, self.user)
        self.assertFalse(cita.analisis_normal)
        self.assertFalse(cita.test_o_sullivan_positivo)
        self.assertTrue(cita.rh_negativo)
        self.assertEqual(cita.observaciones, 'Ninguna')
        self.assertEqual(cita.trimestre, 2)

    def test_actualizar_cita(self):
        cita = CitaExtracciones.objects.get(id=self.cita.id)
        cita.fecha = timezone.make_aware(datetime.datetime(2024, 3, 26, 9, 0, 0), timezone=timezone.get_current_timezone())  
        cita.test_o_sullivan_positivo = True  
        cita.observaciones = 'Nuevas observaciones'  
        cita.save()  

       
        updated_cita = CitaExtracciones.objects.get(id=self.cita.id)

       
        self.assertEqual(updated_cita.fecha, timezone.make_aware(datetime.datetime(2024, 3, 26, 9, 0, 0), timezone=timezone.get_current_timezone()))
        self.assertTrue(updated_cita.test_o_sullivan_positivo)
        self.assertEqual(updated_cita.observaciones, 'Nuevas observaciones')

    
    def test_crear_cita_sin_fecha(self):
      
        client = Client()

        form_data = {
            'usuaria': self.user.id,
            'analisis_normal': False,
            'test_o_sullivan_positivo': False,
            'rh_negativo': True,
            'observaciones': 'Ninguna',
            'trimestre': 2
        }
        form = CitaExtraccionesForm(data=form_data)

      
        self.assertFalse(form.is_valid())
        self.assertTrue('fecha' in form.errors)
    
    def test_eliminar_cita(self):
     
        cita = CitaExtracciones.objects.get(id=self.cita.id)
        cita.delete()

        with self.assertRaises(CitaExtracciones.DoesNotExist):
            CitaExtracciones.objects.get(id=self.cita.id)