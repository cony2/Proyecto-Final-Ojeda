from django.db import models
from django.contrib.auth.models import User


class Pelicula(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    categoria = models.CharField(max_length=100)
    year = models.IntegerField()
    fechaPublicacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=400, default="")
    imagenPortada= models.ImageField(null=True, blank=True, upload_to="imagenes/")

    class Meta:
        ordering = [ '-fechaPublicacion']

    def __str__(self):
        return self.titulo 
    
class Comentario(models.Model):
    comentario = models.ForeignKey(Pelicula, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mensaje = models.TextField(null=True, blank=True)
    fechaComentario = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fechaComentario']

    def __str__(self):
        if self.autor:
            return f'{self.autor.username} - {self.comentario}'
        else:
            return f'None- {self.comentario}'
    
class Avatar(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.FileField(upload_to="media/avatares", null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.imagen}"
