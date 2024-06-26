from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class ConsejosViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_consejos(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('consejos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'consejos.html')


    def test_nauseas(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('nauseas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nauseas.html')


    
    def test_ejercicios(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('ejercicios'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ejercicios.html')


    def test_nutricion(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('nutricion'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nutricion.html')


    def test_lactancia(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('lactancia'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lactancia.html')


    def test_bolso_hospital(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('bolso_hospital'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bolso_hospital.html')

    def test_contracciones(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('contracciones'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contracciones.html')

    def test_induccion_al_parto(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('induccion_al_parto'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'induccion_al_parto.html')


    def test_cordon_umbilical(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('cordon_umbilical'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cordon_umbilical.html')


    def test_suelo_pelvico(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('suelo_pelvico'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'suelo_pelvico.html')
    



    



