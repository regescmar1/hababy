from django import forms



class CitaVacunaForm(forms.Form):
    fecha = forms.DateTimeField(input_formats=['%Y/%m/%d   %H:%M'],  widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    nombre=forms.CharField(required=False)
    observaciones=forms.CharField(widget=forms.Textarea,required=False)
    

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        return fecha
    

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        return nombre
    
    def clean_observaciones(self):
        observaciones = self.cleaned_data['observaciones']
        return observaciones