from django import forms
from .models import Pelicula, Comentario, Avatar
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UserModel

class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ('titulo', 'categoria', 'year', 'descripcion', 'imagenPortada' )
        labels = {'year':'Año', 'titulo':'Película'}
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'cols': 20, 'style': 'vertical-align: top'}),}
        
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('mensaje',)


class EditarPelicula(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = "__all__"
        labels = {'year':'Año', 'titulo':'Película'}
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'cols': 20, 'style': 'vertical-align: top'}),}
        
class UserCreationForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ["username", "email","password1", "password2"]
        help_texts = {k: "" for k in fields}


class UserEditionForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")

    class Meta:
        model = UserModel
        fields = ["email", "password1", "password2", "first_name", "last_name"]
        help_texts = {k: "" for k in fields}


class UserAvatarForm(forms.ModelForm):

    class Meta:
        model = Avatar
        fields = ["imagen"]