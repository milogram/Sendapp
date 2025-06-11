from django import forms
from .models import Usuario, SolicitudCita

class UsuarioForm(forms.Form):
    nombres = forms.CharField(max_length=30, required=True)
    apellidos = forms.CharField(max_length=30, required=True)
    correo = forms.EmailField(required=True)
    telefono = forms.CharField(max_length=20, required=True)
    area = forms.ChoiceField(choices=[
        (1, 'No Aplica'),
        (2, 'Deportes'),
        (3, 'Psicosocial'),
        (4, 'Arte y Cultura'),
        (5, 'Enfermería'),
        (6, 'Líder Social'),
        (7, 'Apoyo Administrativo'),
        (8, 'Apoyo Sostenimiento'),
    ])
    rol = forms.ChoiceField(choices=[
        (1, 'Bienestar'),
        (2, 'Admin'),
        # Agrega más opciones según tus roles disponibles
    ])
    cedula = forms.CharField(max_length=15, required=True)
   
#formulario cita
class SolicitudCitaForm(forms.ModelForm):
    class Meta:
        model = SolicitudCita
        fields = ['area','nombre', 'apellidos', 'telefono', 'email', 'ficha', 'descripcion' ]

        widgets = {
            'hora_cita': forms.TimeInput(attrs={'type': 'time'}),
            'fecha_cita': forms.DateInput(attrs={'type': 'date'}),
        }
        
#Formulario para modificar perfil
class ModificarPerfilForm(forms.ModelForm):
    new_username = forms.CharField(required=False)
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirmar_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Usuario
        fields = ['new_username', 'new_password', 'confirmar_password']

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirmar_password = cleaned_data.get('confirmar_password')
        return cleaned_data

