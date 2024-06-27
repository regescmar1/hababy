
from django import forms
from django.contrib.auth.models import User




class PerfilUsuariaForm(forms.Form):
    username = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(label='New Password', widget=forms.PasswordInput, required=False)
   
    


    def clean_username(self):
        username = self.cleaned_data.get('username')
        usuario_id = self.initial.get('usuario_id')
        if username and User.objects.filter(username=username).exclude(pk=usuario_id).exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        usuario_id = self.initial.get('usuario_id')
        if email and User.objects.filter(email=email).exclude(pk=usuario_id).exists():
            raise forms.ValidationError('Este correo electrónico ya está en uso.')
        return email


