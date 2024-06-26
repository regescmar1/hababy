from django.test import TestCase

import datetime
from django.test import Client, TestCase
from obstetra.models import CitaObstetra
from django.contrib.auth.models import User
from django.utils import timezone

from obstetra.forms.forms import CitaObstetraForm

class ObstetraTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.cita = CitaObstetra.objects.create(
            usuaria=self.user,
            fecha=timezone.make_aware(datetime.datetime(2024, 3, 25, 8, 0, 0), timezone=timezone.get_current_timezone()),  
            peso=70.5,
            altura=1.75,
            imc=23.0,
            tas=120,
            tad=80,
            trimestre=2,
            orden=1,
            observaciones="abc",
            monitores="123"
        )

    def test_crear_cita(self):
        cita = CitaObstetra.objects.get(id=self.cita.id)
        expected_fecha = timezone.make_aware(datetime.datetime(2024, 3, 25, 8, 0, 0), timezone=timezone.get_current_timezone())  
        self.assertEqual(cita.usuaria, self.user)
        fecha=timezone.make_aware(datetime.datetime(2024, 3, 25, 8, 0, 0), timezone=timezone.get_current_timezone()),  
        self.assertAlmostEqual(cita.peso, 70.5)
        self.assertAlmostEqual(cita.altura, 1.75)
        self.assertAlmostEqual(cita.imc, 23.0)
        self.assertEqual(cita.tas, 120)
        self.assertEqual(cita.tad, 80)
        self.assertEqual(cita.trimestre, 2)
        self.assertEqual(cita.orden, 1)
        self.assertEqual(cita.observaciones,"abc")
        self.assertEqual(cita.monitores,"123")
        

    def test_actualizar_cita(self):
        cita = CitaObstetra.objects.get(id=self.cita.id)
        cita.fecha = timezone.make_aware(datetime.datetime(2024, 3, 26, 9, 0, 0), timezone=timezone.get_current_timezone())  
        cita.peso = 60.0  
        cita.altura = 1.6  
        cita.tas = 100 
        cita.tad = 60  
        cita.observaciones="observaciones actualizadas"
        cita.monitores="monitores actualizados"
        cita.save()  
        updated_cita = CitaObstetra.objects.get(id=self.cita.id)

        self.assertEqual(updated_cita.fecha, timezone.make_aware(datetime.datetime(2024, 3, 26, 9, 0, 0), timezone=timezone.get_current_timezone()))
        self.assertEqual(updated_cita.peso,cita.peso)
        self.assertEqual(updated_cita.altura,cita.altura)
        self.assertEqual(updated_cita.tas,cita.tas)
        self.assertEqual(updated_cita.tad,cita.tad)
        self.assertEqual(updated_cita.observaciones,cita.observaciones)
        self.assertEqual(updated_cita.monitores,cita.monitores)

    
    def test_crear_cita_sin_fecha(self):
      
        client = Client()

     
        form_data = {
            'usuaria': self.user.id,
            'peso': 70.5,
            'altura': 1.75,
            'tas': 120,
            'tad': 80,
            'trimestre': 2,
            'orden': 1,
            'observaciones':"abc",
            'monitores':"123"
        }
        form = CitaObstetraForm(data=form_data)

     
        self.assertFalse(form.is_valid())

        self.assertTrue('fecha' in form.errors)
    

    def test_eliminar_cita(self):
        cita = CitaObstetra.objects.get(id=self.cita.id)
        cita.delete()
        with self.assertRaises(CitaObstetra.DoesNotExist):
            CitaObstetra.objects.get(id=self.cita.id)