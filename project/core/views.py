from django.shortcuts import render, redirect
from .models import Pelicula, Comentario, Avatar
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import PeliculaForm, ComentarioForm, EditarPelicula, UserCreationForm, UserEditionForm, UserAvatarForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        usuario = request.user
        avatar = Avatar.objects.filter(user=usuario).last()
        avatar_url = avatar.imagen.url if avatar is not None else ""
    else:
        avatar_url = ""

    return render(request, "core/index.html", context={"avatar_url":avatar_url})

def about(request):
    return render(request, "core/acerca_de_mi.html")


class PeliculaList(ListView): 

    model = Pelicula
    template_name = "core/peliculas_list.html"
    context_object_name = "peliculas"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            usuario = self.request.user
            avatar_url = obtener_avatar_url(usuario)
            context['avatar_url'] = avatar_url
        return context

class PeliculaDetail(DetailView):
    model = Pelicula
    template_name = "core/pelicula_detail.html"
    context_object_name = "pelicula"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pelicula = self.get_object()
        comentarios = Comentario.objects.filter(comentario=pelicula)
        print(comentarios)

        context['comentarios'] = comentarios
        return context

    
class PeliculaCreate(CreateView):
    model = Pelicula
    form_class = PeliculaForm
    template_name = "core/pelicula_create.html"
    success_url = reverse_lazy("core:lista-peliculas")
    
    def form_valid(self, form):
        form.instance.autor = self.request.user  # Asignar el usuario actual como autor
        return super().form_valid(form)

    

class PeliculaUpdate(UpdateView):
    model = Pelicula
    template_name = "core/pelicula_update.html"
    form_class = EditarPelicula
    context_object_name = 'editar_pelicula'
    success_url = reverse_lazy("core:lista-peliculas")

class PeliculaDelete(DeleteView):
    model = Pelicula
    template_name = "core/pelicula_delete.html"
    success_url = reverse_lazy("core:lista-peliculas")

class ComentarioCreate( CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'core/comentario.html'
    success_url = reverse_lazy('core:lista-peliculas')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.comentario_id = self.kwargs['pk']
        return super(ComentarioCreate, self).form_valid(form)
    

    




##LOGIN / LOGOUT
def registro_view(request):
    if request.method == "GET":
        return render(request, "core/registro.html", {"form": UserCreationForm()})
    else:
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            usuario = informacion["username"]
            formulario.save()

            return render(
                request,
                "core/index.html",
                {"mensaje": f"Te registraste correctamente, {usuario}!"}
            )
        else:
            return render(
                request,
                "core/registro.html",
                {"form": formulario}
            )

def login_view(request):
    if request.user.is_authenticated:
        return render(
            request,
            "core/index.html",
            {"mensaje": f"Ya estás autenticado: {request.user.username}"}
        )

    if request.method == "GET":
        return render(
            request,
            "core/login.html",
            {"form": AuthenticationForm()}
        )
    else:
        formulario = AuthenticationForm(request, data=request.POST)

        if formulario.is_valid():
            informacion = formulario.cleaned_data
            usuario = informacion["username"]
            password = informacion["password"]

            modelo = authenticate(username=usuario, password=password)
            login(request, modelo)

            return render(
                request,
                "core/index.html",
                {"mensaje": f"Bienvenido {request.user.username}"}
            )
        else:
            return render(
                request,
                "core/login.html",
                {"form": formulario}
            )

@login_required
def editar_perfil_view(request):

    usuario = request.user
    avatar = Avatar.objects.filter(user=usuario).last()
    avatar_url = avatar.imagen.url if avatar is not None else ""


    if request.method == "GET":


        valores_iniciales = {
            "email": usuario.email,
            "first_name": usuario.first_name,
            "last_name": usuario.last_name
        }


        formulario = UserEditionForm(initial=valores_iniciales)
        return render(
            request,
            "core/editar_perfil.html",
            context={"form": formulario, "usuario": usuario, "avatar_url": avatar_url}
            )
    else:
        formulario = UserEditionForm(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            usuario.email = informacion["email"]
            usuario.set_password(informacion["password1"])
            usuario.first_name = informacion["first_name"]
            usuario.last_name = informacion["last_name"]
            usuario.save()
        return redirect("core:index")



def crear_avatar_view(request):

    usuario = request.user

    if request.method == "GET":
        formulario = UserAvatarForm()
        return render(
            request,
            "core/crear_avatar.html",
            context={"form": formulario, "usuario": usuario}
        )
    else:
        formulario = UserAvatarForm(request.POST, request.FILES)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            modelo = Avatar(user=usuario, imagen=informacion["imagen"])
            modelo.save()
            return redirect("core:index")


def obtener_avatar_url(usuario):
    avatar = Avatar.objects.filter(user=usuario).last()
    return avatar.imagen.url if avatar is not None else ""    



