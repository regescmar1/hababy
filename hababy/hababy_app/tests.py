from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.
class HababyAppTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_principal(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('principal'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'principal.html')


    def test_acerca_de(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('acerca_de'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'acerca_de.html')


    
    def test_contacto(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('contacto'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacto.html')


    def test_politica_privacidad(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('politica_privacidad'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'politica_privacidad.html')