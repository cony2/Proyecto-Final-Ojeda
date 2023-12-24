from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import PeliculaCreate, PeliculaList, PeliculaDetail, PeliculaUpdate, PeliculaDelete,registro_view, login_view, editar_perfil_view, crear_avatar_view
from django.contrib.auth.views import LogoutView

app_name = "core"

urlpatterns = [
    path("", views.home, name="index"),
    path("acerca-de-mi/", views.about, name="about"),
    path("lista-peliculas/", PeliculaList.as_view(), name="lista-peliculas"),
    path("detalle-pelicula/<int:pk>/", PeliculaDetail.as_view(), name="detalle-pelicula"),
    path("crear-pelicula/", PeliculaCreate.as_view(), name="crear-pelicula"),
    path("editar-pelicula/<int:pk>/", PeliculaUpdate.as_view(), name="editar-pelicula"),
    path("eliminar-pelicula/<int:pk>/", PeliculaDelete.as_view(), name="eliminar-pelicula"),
    path('detalle-pelicula/<int:pk>/comentar/', views.ComentarioCreate.as_view() , name='comentario'),

    path("registro", registro_view, name="registro"),
    path("login", login_view, name="login"),
    path("logout", LogoutView.as_view(template_name="core/logout.html"), name="logout"),
    path("editar-perfil", editar_perfil_view, name="editar-perfil"),
    path("crear-avatar", crear_avatar_view, name="crear-avatar")
    

]
    
    

