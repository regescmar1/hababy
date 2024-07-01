from django import forms

class SesionForm(forms.Form):
    fecha = forms.DateTimeField(input_formats=['%Y/%m/%d   %H:%M'],  widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    titulo=forms.CharField()
    observaciones=forms.CharField(widget=forms.Textarea,required=False)

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        return fecha
    
    def clean_titulo(self):
        titulo = self.cleaned_data['titulo']
        return titulo

    def clean_observaciones(self):
        observaciones = self.cleaned_data['observaciones']
        return observaciones