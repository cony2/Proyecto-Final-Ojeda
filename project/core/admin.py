from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Pelicula)
admin.site.register(models.Comentario)
admin.site.register(models.Avatar)