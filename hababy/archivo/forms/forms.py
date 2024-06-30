from django import forms
from django.core.exceptions import ValidationError


class ArchivoForm(forms.Form):
    archivo=forms.ImageField(required=False,max_length=255)
    def clean_archivo(self):
        archivo = self.cleaned_data['archivo']
        if archivo:
            # Verificar si el archivo subido no es una imagen
            if not archivo.content_type.startswith('image'):
                raise ValidationError("El archivo subido no es una imagen válida.")
        else:
            # Si no se ha subido ningún archivo, no hay errores
            return archivo
        return archivo
    

